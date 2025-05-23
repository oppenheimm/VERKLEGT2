from django.db import models
from django.conf import settings
from users.models import User
from core.storage import DatabaseStorage
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('duplex', 'Duplex'),
        ('studio', 'Studio'),
        ('land', 'Land'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=20, default="000")
    sqft = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    year_built = models.IntegerField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE_CHOICES,
        default='apartment'
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='properties',
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        related_name="items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def property_main_image_path(instance, filename):
        return f"property_photos/{instance.id}/{filename}"

    main_image = models.ImageField(
        upload_to=property_main_image_path,
        storage=DatabaseStorage(),
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        if (self.latitude is None or self.longitude is None) and self.address and self.city:
            try:
                geolocator = Nominatim(user_agent="django-real-estate-app")
                location = geolocator.geocode(f"{self.address}, {self.zip_code} {self.city}")
                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
            except GeocoderTimedOut:
                pass  # Optionally, retry here or log timeout

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="property_photos/")
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class PurchaseOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ("finalized", "Finalized"),
    ]

    property = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='offers')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    updated_at  = models.DateTimeField(auto_now=True)
    is_resubmission = models.BooleanField(default=False)
    status      = models.CharField(max_length=10,
                                   choices=STATUS_CHOICES,
                                   default='pending')

    def __str__(self):
        return f"Offer by {self.buyer.username} for {self.amount} kr on {self.property.title}"