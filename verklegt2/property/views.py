from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Property, PropertyImage
from .forms import PropertyForm


def property_list(request):
    properties = Property.objects.filter(is_published=True)
    return render(request, "property/list.html", {"properties": properties})


def property_detail(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, "property/detail.html", {"property": property_obj})


@login_required
def property_create(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            # attach current user before first save
            property_instance = form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()

            # handle extra images
            for f in request.FILES.getlist("extra_images"):
                PropertyImage.objects.create(property=property_instance, image=f)

            messages.success(request, "Property created successfully.")
            return redirect("property:list")
    else:
        form = PropertyForm()

    return render(request, "property/create.html", {"form": form})


@require_POST
@login_required
def property_delete(request, id):
    property_obj = get_object_or_404(Property, id=id)
    if property_obj.owner != request.user:
        return HttpResponseForbidden("You can’t delete this listing.")

    property_obj.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect("property:list")
