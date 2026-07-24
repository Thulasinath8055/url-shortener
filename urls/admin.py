from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    """
    Customizes how ShortURL appears in the Django Admin panel.
    """
    # Columns displayed in the list view
    list_display = ('short_code', 'user', 'original_url', 'click_count', 'created_at')

    # Fields that appear as clickable links
    list_display_links = ('short_code',)

    # Adds a search bar that searches these fields
    search_fields = ('short_code', 'original_url')

    # Adds filter sidebar by user and date
    list_filter = ('user', 'created_at')

    # Fields that should be read-only (never editable in admin)
    readonly_fields = ('click_count', 'created_at')