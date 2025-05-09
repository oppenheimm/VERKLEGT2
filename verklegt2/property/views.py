from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, PropertyImage
from .forms import PropertyForm
from django.views.decorators.http import require_POST
from django.contrib import messages


def property_list(request):
    properties = Property.objects.filter(is_published=True)
    return render(request, 'property/list.html', {'properties': properties})

def property_detail(request, id):
    property_obj = get_object_or_404(Property, id=id)
    return render(request, 'property/detail.html', {'property': property_obj})

def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_instance = form.save()

            # Save extra images from <input name="extra_images" multiple>
            for f in request.FILES.getlist('extra_images'):
                PropertyImage.objects.create(property=property_instance, image=f)

            return redirect('property:list')
    else:
        form = PropertyForm()

    return render(request, 'property/create.html', {'form': form})

@require_POST
def property_delete(request, id):
    property_obj = get_object_or_404(Property, id=id)
    property_obj.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('property:list')