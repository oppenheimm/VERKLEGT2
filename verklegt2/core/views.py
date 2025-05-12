from django.shortcuts import render, redirect
from property.models import Category, Property
from property.models import Property
from django.contrib.auth import logout


def index(request):
    featured_properties = Property.objects.filter(is_published=True)[:6]

    all_types = sorted(set(Property.objects.values_list('type', flat=True)))
    all_cities = sorted(set(Property.objects.values_list('city', flat=True)))

    return render(request, 'core/index.html', {
        'featured_properties': featured_properties,
        'all_types': all_types,
        'all_cities': all_cities,
    })


def contact(request):
    return render(request, "core/contact.html")
