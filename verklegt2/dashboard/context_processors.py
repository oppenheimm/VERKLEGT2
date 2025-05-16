from property.models import PurchaseOffer 

def notification_context(request):
    has_notifications = False
    if request.user.is_authenticated:
        seller_has = PurchaseOffer.objects.filter(property__owner=request.user).exists()
        buyer_has = PurchaseOffer.objects.filter(buyer=request.user).exists()
        has_notifications = seller_has or buyer_has
    return {'has_notifications': has_notifications}