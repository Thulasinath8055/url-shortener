from django.shortcuts import get_object_or_404, redirect
from django.db.models import F
from rest_framework import generics, permissions
from rest_framework.views import APIView

from .models import ShortURL
from .serializers import ShortURLSerializer

# =============================================================================
# 1. LIST & CREATE URLS (GET /api/urls/, POST /api/urls/)
# =============================================================================

class ShortURLListCreateView(generics.ListCreateAPIView):
    """
    GET  -> Returns all short URLs created by the authenticated user.
    POST -> Accepts {'original_url': 'https://...'} and creates a new ShortURL.
    
    The user is automatically attached in the serializer's create() method.
    The short code is auto-generated. The response includes the full short_link.
    """
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Override to enforce ownership.
        Even if a user guesses another user's URL ID, they will never see it
        because the queryset is filtered to their own records.
        """
        return ShortURL.objects.filter(user=self.request.user)

# =============================================================================
# 2. DELETE URL (DELETE /api/urls/<id>/)
# =============================================================================

class ShortURLDeleteView(generics.DestroyAPIView):
    """
    DELETE -> Removes a specific short URL by its primary key (id).
    
    Users can only delete their own URLs. Attempting to delete another user's
    URL returns a 404 (we intentionally do NOT reveal that the URL exists).
    """
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Same ownership filter as above. If the pk is not in this queryset,
        Django automatically raises Http404.
        """
        return ShortURL.objects.filter(user=self.request.user)

# =============================================================================
# 3. REDIRECT (GET /<short_code>/)
# =============================================================================

class ShortURLRedirectView(APIView):
    """
    Public endpoint. Anyone can visit a short link without authentication.
    
    Flow:
    1. Look up the ShortURL by its short_code.
    2. Atomically increment the click_count using F() expression.
    3. Redirect the browser to the original_url.
    """
    # Explicitly disable authentication for this endpoint.
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, short_code, *args, **kwargs):
        # Step 1: Fetch the URL or return 404 if code doesn't exist.
        short_url = get_object_or_404(ShortURL, short_code=short_code)

        # Step 2: ATOMIC increment.
        # F('click_count') tells PostgreSQL: "SET click_count = click_count + 1"
        # This happens INSIDE the database, so even if 1000 people click
        # simultaneously, every click is counted correctly.
        ShortURL.objects.filter(pk=short_url.pk).update(
            click_count=F('click_count') + 1
        )

        # Step 3: Redirect browser to the destination.
        # redirect() returns an HTTP 302 Found response by default.
        return redirect(short_url.original_url)