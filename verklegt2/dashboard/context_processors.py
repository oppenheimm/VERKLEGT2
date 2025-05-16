from property.models import PurchaseOffer 

def notification_context(request):
    has_notifications = False
    if request.user.is_authenticated:
        has_notifications = PurchaseOffer.objects.filter(property__owner=request.user).exists()
        
        if not has_notifications:
            has_notifications = PurchaseOffer.objects.filter(buyer=request.user).exists()
        
    return {'has_notifications': has_notifications}