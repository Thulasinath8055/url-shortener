from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import RegisterView

"""
Project-level URL routing table.

Order matters: Django checks each pattern top-to-bottom until it finds a match.
/admin/ and /api/ are matched before the root-level short code redirect.
"""

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # -------------------------------------------------------------
    # AUTHENTICATION ENDPOINTS
    # -------------------------------------------------------------
    # We define these directly here (instead of include()) to ensure
    # they live exactly at /api/register/, /api/login/, etc.
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # -------------------------------------------------------------
    # URL SHORTENER APP
    # -------------------------------------------------------------
    # Includes /api/urls/ and /<short_code>/ from urls/urls.py
    path('', include('urls.urls')),

    # -------------------------------------------------------------
    # API DOCUMENTATION (Swagger)
    # -------------------------------------------------------------
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]