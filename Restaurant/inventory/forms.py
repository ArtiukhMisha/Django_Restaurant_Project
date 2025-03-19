from .models import Purchase, MenuItem, Ingridient, RecipeRequirement
from django import forms
from django.forms import (
    ModelForm,
    SelectMultiple,
    TextInput,
    NumberInput,
    Select,
    Textarea,
    CheckboxSelectMultiple,
)


class MenuForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "form-control", "placeholder": "Name"}),
            "price": NumberInput(
                attrs={"class": "form-control", "default": 0.0, min: 0}
            ),
        }


class RecipeRequirementForm(forms.Form):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingridient.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
    )
    quantities = forms.CharField(widget=forms.HiddenInput(), required=False)
