from django import forms
from .models import PurchaseFinalization

class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = ['full_name', 'national_id', 'street_name', 'city', 'postal_code', 'country']
        widgets = {
            'country': forms.Select(choices=[
                ('Iceland', 'Iceland'),
                ('Sweden', 'Sweden'),
                ('Denmark', 'Denmark'),
                ('Norway', 'Norway'),
                ('Finland', 'Finland'),
            ])
        }

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={
                'class': 'block w-2/3 mt-1 border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500'
            })
        }

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = ['cardholder_name', 'card_number', 'expiry_date', 'cvc']

class BankTransferForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = ['account_holder_name', 'iban', 'bank_name']

class MortgageForm(forms.ModelForm):
    class Meta:
        model = PurchaseFinalization
        fields = ['mortgage_provider', 'loan_amount', 'interest_rate', 'approval_code']
