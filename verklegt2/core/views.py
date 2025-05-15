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

import mimetypes
from django.apps import apps
from django.http import Http404, HttpResponse
from django.utils.encoding import smart_str


def serve_db_file(request, file_path: str):
    """
    Stream a FileBlob to the browser.
    URL pattern:  /db-files/<path:file_path>
    """
    FileBlob = apps.get_model("core", "FileBlob")
    try:
        blob = FileBlob.objects.get(path=file_path)
    except FileBlob.DoesNotExist:
        raise Http404(f"{file_path!r} not found in FileBlob")

    content_type, _ = mimetypes.guess_type(blob.path)
    response = HttpResponse(blob.data, content_type=content_type or "application/octet-stream")
    response["Content-Disposition"] = f'inline; filename="{smart_str(blob.path.split("/")[-1])}"'
    return response
