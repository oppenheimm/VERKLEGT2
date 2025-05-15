import uuid
from django.db import models
from .storage import DatabaseStorage


class FileBlob(models.Model):
    """
    Universal binary-large-object table.
    """
    path = models.CharField(max_length=400, unique=True)
    data = models.BinaryField()
    content_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.path


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def property_main_image_path(instance: "Property", filename: str) -> str:
    """
    Use a random UUID instead of PK (which is None on first save).
    """
    return f"property_photos/{uuid.uuid4().hex}/{filename}"


# ------------------------------------------------------------------
# Domain models
# ------------------------------------------------------------------
class Property(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    main_image = models.ImageField(
        upload_to=property_main_image_path,
        storage=DatabaseStorage(),      # ← ensures DB storage even if global setting changes
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.title


class PropertyImage(models.Model):
    """
    Additional gallery images for a property.
    """
    property = models.ForeignKey(
        Property, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="property_photos/",
        storage=DatabaseStorage(),      # ← every gallery image goes to the DB
    )

    def __str__(self) -> str:
        return f"{self.property.title} — {self.id}"
