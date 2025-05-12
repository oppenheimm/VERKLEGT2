from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Property, PropertyImage, PurchaseOffer
from .forms import PropertyForm, EditPropertyForm, PurchaseOfferForm


def property_list(request):
    properties = Property.objects.all()

    # Only show unsold properties by default
    show_sold = request.GET.get('show_sold') == 'on'
    if not show_sold:
        properties = properties.filter(is_sold=False)

    # Unique sorted types for dropdown
    all_types = sorted(set(Property.objects.values_list('type', flat=True)))

    # Bedrooms for dropdown
    all_bedrooms = sorted(set(Property.objects.values_list('bedrooms', flat=True)))

    # Zip codes for dropdown
    all_zip_codes = sorted(set(Property.objects.values_list('zip_code', flat=True)))
    
    all_cities = sorted(set(Property.objects.values_list('city', flat=True)))

    # Filter by zip code
    zip_code = request.GET.get('zip_code')
    if zip_code:
        properties = properties.filter(zip_code=zip_code)
    
    selected_city = request.GET.get('city')
    if selected_city:
        properties = properties.filter(city=selected_city)

    # Filter by type
    selected_type = request.GET.get('type')
    if selected_type:
        properties = properties.filter(type=selected_type)

    # Bedrooms
    bedrooms = request.GET.get('bedrooms')
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)

    # Sqft range
    min_sqft = request.GET.get('min_sqft')
    if min_sqft:
        properties = properties.filter(sqft__gte=min_sqft)

    max_sqft = request.GET.get('max_sqft')
    if max_sqft:
        properties = properties.filter(sqft__lte=max_sqft)

    # Price range
    min_price = request.GET.get('min_price')
    if min_price:
        properties = properties.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        properties = properties.filter(price__lte=max_price)

    # Search street
    query = request.GET.get('q')
    if query:
        properties = properties.filter(address__icontains=query)

    # Order by
    order_by = request.GET.get('order_by')
    if order_by in ['price', 'title']:
        properties = properties.order_by(order_by)

    context = {
        'properties': properties,
        'all_types': all_types,
        'selected_type': selected_type,
        'all_bedrooms': all_bedrooms,
        'all_cities': all_cities,
        'all_zip_codes': all_zip_codes,
        'request': request,  # pass full request for form prefills
    }

    return render(request, 'property/list.html', context)


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

