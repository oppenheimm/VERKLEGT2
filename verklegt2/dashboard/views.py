from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from property.models import Property, PurchaseOffer

@login_required
def dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    offers = PurchaseOffer.objects.filter(property__in=properties).select_related('property', 'buyer')

    return render(request, 'dashboard/dashboard.html', {
        'properties': properties,
        'offers': offers,
    })
