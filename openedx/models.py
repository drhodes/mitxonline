"""Courseware models"""
from django.conf import settings
from django.db import models
from mitol.common.models import TimestampedModel

from openedx.constants import OPENEDX_PLATFORM_CHOICES, PLATFORM_EDX


class OpenEdxUser(TimestampedModel):
    """Model representing a User in a openedx platform"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="openedx_users",
    )
    platform = models.CharField(
        max_length=20, choices=OPENEDX_PLATFORM_CHOICES, default=PLATFORM_EDX
    )
    has_been_synced = models.BooleanField(
        default=True,
        help_text="Indicates whether a corresponding user has been created on the openedx platform",
    )

    def __str__(self):
        return f"OpenEdxUser for {self.user} in {self.platform}"

    class Meta:
        unique_together = ("user", "platform")


class OpenEdxApiAuth(TimestampedModel):
    """Model that stores OAuth2 tokens for authenticating Open edX API calls"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="openedx_api_auth",
    )

    refresh_token = models.CharField(max_length=128)
    access_token = models.CharField(null=True, max_length=128)
    access_token_expires_on = models.DateTimeField(null=True)

    def __str__(self):
        return f"OpenEdxApiAuth for {self.user}"

    class Meta:
        index_together = ("user", "access_token_expires_on")
