# accounts/models.py

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from core.storage import DatabaseStorage


def user_profile_image_path(instance, filename):

    return f"profile_images/user_{instance.id}/{filename}"


def user_logo_image_path(instance, filename):
    return f"profile_logos/user_{instance.id}/{filename}"


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Fields:
      - username (inherited)
      - email (unique)
      - password (inherited)
      - name (full name)
      - profile_image
      - user_type (buyer, individual_seller, agency_seller)
    """

    # User types
    ADMIN = "admin"
    BUYER = "buyer"
    INDIVIDUAL_SELLER = "individual_seller"
    AGENCY_SELLER = "agency_seller"
    USER_TYPE_CHOICES = [
        (ADMIN, "Admin"),
        (BUYER, "Buyer"),
        (INDIVIDUAL_SELLER, "Individual Seller"),
        (AGENCY_SELLER, "Agency Seller"),
    ]

    # Core fields
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField("email address", unique=True)
    name = models.CharField("full name", max_length=255, blank=True)

    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        storage=DatabaseStorage(),
        blank=True,
        null=True,
        help_text="Upload a profile picture.",
    )

    # Distinguish between buyer and seller types
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=BUYER,
        help_text="Designates the type of user.",
    )

    # Use username as the unique identifier
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "user_type", "name"]

    def __str__(self):
        return self.username


class BuyerProfile(models.Model):
    """
    Profile data specific to buyers.
    One-to-one relationship with User where user_type == BUYER.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="buyer_profile"
    )
    saved_searches = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"BuyerProfile for {self.user.username}"


class SellerProfile(models.Model):
    """Extended information for sellers (individual or agency)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="seller_profile",
    )

    street = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    logo = models.ImageField(
        upload_to=user_logo_image_path,
        storage=DatabaseStorage(),
        blank=True,
        null=True,
        help_text="Your company logo—also stored in the database.",
    )
    bio = models.TextField(blank=True)

    # Existing fields
    company_name = models.CharField(max_length=255, blank=True)
    license_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"SellerProfile for {self.user.username}"

    @property
    def is_agency(self):
        return self.user.user_type == User.AGENCY_SELLER

    @property
    def address_display(self):
        if self.is_agency:
            return f"{self.street}, {self.city} {self.postal_code}".strip()
        return ""
