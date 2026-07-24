from django.urls import path
from .views import ShortURLListCreateView, ShortURLDeleteView, ShortURLRedirectView

"""
URL routing for the 'urls' app.

These patterns are included in the project's root URLconf under specific paths.
Because of Django's URL resolution order, these are combined intelligently
so the redirect does not conflict with /admin/ or /api/ routes.
"""

urlpatterns = [
    # GET /api/urls/  -> List
    # POST /api/urls/ -> Create
    path('urls/', ShortURLListCreateView.as_view(), name='url-list-create'),

    # DELETE /api/urls/<id>/ -> Delete
    path('urls/<int:pk>/', ShortURLDeleteView.as_view(), name='url-delete'),

    # GET /<short_code>/ -> Redirect (public)
    path('<str:short_code>/', ShortURLRedirectView.as_view(), name='url-redirect'),
]