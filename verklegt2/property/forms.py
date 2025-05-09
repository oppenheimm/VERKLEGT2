# property/forms.py
from django import forms
from .models import Property, PropertyImage

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['owner', 'title', 'description', 'price', 'address', 'city', 'zip_code',
                  'sqft', 'bedrooms', 'bathrooms', 'is_published', 'is_sold',
                  'category', 'main_image']
