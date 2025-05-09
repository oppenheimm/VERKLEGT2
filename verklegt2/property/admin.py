from django.contrib import admin

from .models import Property, Category, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "city",
        "price",
        "is_published",
        "owner",
        "created_at",
    )
    list_filter = ("is_published", "is_sold", "owner", "city", "created_at")
    search_fields = ("title", "city", "address", "owner__username")
    inlines = [PropertyImageInline]


admin.site.register(Category)
admin.site.register(Property, PropertyAdmin)
