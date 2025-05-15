from django.db import models

class PurchaseFinalization(models.Model):
    offer = models.OneToOneField('property.PurchaseOffer', on_delete=models.CASCADE)

    # Contact information
    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20)
    street_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    # Payment choice
    payment_method = models.CharField(max_length=20, choices=[
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('mortgage', 'Mortgage'),
    ])

    # Credit card
    cardholder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.CharField(max_length=7, blank=True, null=True)
    cvc = models.CharField(max_length=4, blank=True, null=True)

    # Bank transfer
    account_holder_name = models.CharField(max_length=100, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)
    bank_name = models.CharField(max_length=34, blank=True, null=True)

    # Mortgage
    mortgage_provider = models.CharField(max_length=100, blank=True, null=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    approval_code = models.CharField(max_length=20, blank=True, null=True)

    is_confirmed = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Finalization for offer {self.offer.id}"
