# property/forms.py
from django import forms
from .models import Property, PropertyImage, PurchaseOffer
from django.utils.safestring import mark_safe


class TailwindMixin:
    def apply_tailwind(self):
        for visible in self.visible_fields():
            if hasattr(visible.field.widget, 'input_type') and visible.field.widget.input_type == 'checkbox':
                visible.field.widget.attrs.update({'class': 'rounded text-blue-600 focus:ring-blue-500 mb-4'})
            else:
                visible.field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4'
                })

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'type', 'address', 'city',
            'zip_code', 'bedrooms', 'bathrooms', 'sqft', 'year_built', 'main_image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'type': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-md'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
            })


class EditPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'type', 'address', 'city', 'zip_code', 'bedrooms', 'bathrooms', 'sqft', 'year_built', 'main_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'main_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            if field.name != 'main_image':  # Already styled above
                field.field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500'
                })


class PurchaseOfferForm(forms.ModelForm):
    amount = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
            'placeholder': 'Offer Amount'
        }),
        label=mark_safe("Offer Amount <span class='text-sm text-gray-500'>(in ISK)</span>")
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
            'placeholder': 'Your Message'
        }),
        label=mark_safe("Message <span class='text-sm text-gray-500'>(required)</span>")
    )
    
    expiration_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
            'placeholder': 'Expiration Date (YYYY-MM-DD)'
        }),
        label=mark_safe("Expiration Date <span class='text-sm text-gray-500'>(optional)</span>")
    )
    
    class Meta:
        model = PurchaseOffer
        fields = ['amount', 'message', 'expiration_date']
            