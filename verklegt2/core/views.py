from django.shortcuts import render, redirect
from property.models import Category, Property
from property.models import Property
from django.contrib.auth import logout


def index(request):
    properties = Property.objects.filter(is_published=True, is_sold=False)[:6]
    categories = Category.objects.all()
    context = {
        "featured_properties": properties,
        "categories": categories,
    }
    return render(request, "core/index.html", context)


def contact(request):
    return render(request, "core/contact.html")
