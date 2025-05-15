from django import forms
from .models import Property, PropertyImage


# ---------------------------- Tailwind mixin ----------------------------
class TailwindMixin:
    """
    Applies Tailwind CSS classes to every field widget.
    """

    def apply_tailwind(self):
        base = (
            "block w-full px-3 py-2 border rounded-lg "
            "focus:outline-none focus:ring-2 focus:ring-blue-500"
        )
        for field in self.fields.values():
            old = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{old} {base}".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


# ---------------------------- Model forms ----------------------------
class PropertyForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            "title",
            "description",
            "price",
            "main_image",
        ]


class PropertyImageForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ["image"]
