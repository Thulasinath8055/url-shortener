from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

"""
Project-level URL routing table.

We keep this file minimal. Later, each app (accounts, urls) will define its own
urls.py, and we will 'include()' them here. For now, we just wire up the admin
and automatic Swagger documentation so we can verify our setup.
"""

urlpatterns = [
    # Django Admin panel
    path('admin/', admin.site.urls),

    # Raw OpenAPI 3.0 schema (JSON). drf-spectacular generates this automatically.
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Human-friendly Swagger UI. It reads the schema above and renders it.
    # 'url_name='schema'' links this view to the /api/schema/ endpoint.
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]