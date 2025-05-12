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


@login_required
def notifications(request):
    user = request.user
    owner_offers = []
    buyer_offers = []

    if user.user_type == 'agency_seller' or user.user_type == 'individual_seller':
        owner_offers = PurchaseOffer.objects.filter(property__owner=user).select_related('property', 'buyer')

    if user.user_type == 'buyer':
        buyer_offers = PurchaseOffer.objects.filter(buyer=user).select_related('property')

    return render(request, 'dashboard/notifications.html', {
        'owner_offers': owner_offers,
        'buyer_offers': buyer_offers,
    })