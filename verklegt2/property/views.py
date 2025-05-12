from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Property, PropertyImage, PurchaseOffer
from .forms import PropertyForm, EditPropertyForm, PurchaseOfferForm


def property_list(request):
    properties = Property.objects.filter(is_published=True)
    return render(request, "property/list.html", {"properties": properties})


def property_detail(request, id):
    property_obj = get_object_or_404(Property, id=id, is_published=True)

    # fetch other properties with the same zip code (excluding current)
    related_properties = Property.objects.filter(
        zip_code=property_obj.zip_code,
        is_published=True
    ).exclude(id=property_obj.id)

    return render(
        request,
        "property/detail.html",
        {
            "property": property_obj,
            "related_properties": related_properties
        }
    )


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

@login_required
def toggle_property_sold(request, pk):
    property = get_object_or_404(Property, pk=pk, owner=request.user)
    property.is_sold = not property.is_sold
    property.save()
    return redirect('property:detail', id=pk)

@login_required
def edit_property(request, id):
    property = get_object_or_404(Property, pk=id, owner=request.user)

    if request.method == 'POST':
        form = EditPropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()

            # Handle image deletions
            delete_ids = request.POST.getlist('delete_image_ids')
            if delete_ids:
                property.images.filter(id__in=delete_ids).delete()

            # Handle new uploads
            for image_file in request.FILES.getlist('extra_images'):
                PropertyImage.objects.create(property=property, image=image_file)

            return redirect('property:detail', id=property.id)
    else:
        form = EditPropertyForm(instance=property)

    return render(request, 'property/edit_property.html', {
        'form': form,
        'property': property
    })


@login_required
def make_offer(request, property_id):
    property_obj = get_object_or_404(Property, pk=property_id)

    if request.user.user_type != 'buyer':
        return redirect('property:detail', property_id)

    if request.method == 'POST':
        form = PurchaseOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.property = property_obj
            offer.buyer = request.user
            offer.save()
            return redirect('property:detail', property_id)
    else:
        form = PurchaseOfferForm()

    return render(request, 'property/make_offer.html', {'form': form, 'property': property_obj})


@login_required
def accept_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__owner=request.user)

    offer.status = 'accepted'
    offer.save()

    # Mark property as sold
    property_obj = offer.property
    property_obj.is_sold = True
    property_obj.save()

    # Decline other offers for this property
    PurchaseOffer.objects.filter(property=property_obj).exclude(id=offer_id).update(status='declined')

    return redirect('dashboard:dashboard')


@login_required
def decline_offer(request, offer_id):
    offer = get_object_or_404(PurchaseOffer, id=offer_id, property__owner=request.user)
    offer.status = 'declined'
    offer.save()
    return redirect('dashboard:dashboard')