from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = [
            "name",
        ]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    is_sold = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, related_name="items", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="item_images", blank=True, null=True)

    class Meta:
        ordering = [
            "name",
        ]

    def __str__(self):
        return self.name
