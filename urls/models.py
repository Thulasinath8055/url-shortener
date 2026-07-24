from django.db import models
from django.contrib.auth.models import User

class ShortURL(models.Model):
    """
    Represents a shortened URL created by a registered user.
    """

    # -------------------------------------------------------------------------
    # 1. RELATIONSHIPS
    # -------------------------------------------------------------------------

    # ForeignKey links this ShortURL to the Django User who created it.
    # on_delete=CASCADE means: if the User is deleted, delete all their URLs.
    # related_name='short_urls' lets us write: user.short_urls.all()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='short_urls'
    )

    # -------------------------------------------------------------------------
    # 2. URL FIELDS
    # -------------------------------------------------------------------------

    # The full original URL that the short link redirects to.
    # max_length=2048 covers almost any URL in the wild.
    original_url = models.URLField(max_length=2048)

    # The unique short code (e.g., "a3f9k2"). This is what users share.
    # unique=True: database enforces no duplicates.
    # db_index=True: speeds up lookups by short_code massively.
    short_code = models.CharField(max_length=10, unique=True, db_index=True)

    # -------------------------------------------------------------------------
    # 3. ANALYTICS FIELDS
    # -------------------------------------------------------------------------

    # Tracks how many times the short link has been clicked.
    # Default is 0 because every new link starts with zero clicks.
    click_count = models.PositiveIntegerField(default=0)

    # -------------------------------------------------------------------------
    # 4. METADATA FIELDS
    # -------------------------------------------------------------------------

    # auto_now_add=True sets this to the current timestamp ONCE when created.
    created_at = models.DateTimeField(auto_now_add=True)

    # -------------------------------------------------------------------------
    # 5. META & STRING REPRESENTATION
    # -------------------------------------------------------------------------

    class Meta:
        # Orders queries by newest first by default.
        # So /api/urls/ returns the user's most recent links first.
        ordering = ['-created_at']

        # Human-readable name in the Django admin panel.
        verbose_name = 'Short URL'
        verbose_name_plural = 'Short URLs'

    def __str__(self):
        # What we see in the admin panel and shell.
        return f"{self.short_code} → {self.original_url}"