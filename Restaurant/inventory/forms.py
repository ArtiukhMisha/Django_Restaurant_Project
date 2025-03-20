from .models import Purchase, MenuItem, Ingredient, RecipeRequirement
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
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name",
                    "required": "required",
                },
            ),
            "price": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Price",
                    "name": "price",
                    "required": "required",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        self.fields["price"].initial = None


class ItemForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name",
                    "required": "required",
                },
            ),
            "quantity": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Quantity",
                    "name": "quantity",
                    "required": "required",
                    "min": 0,
                }
            ),
            "unit": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Unit",
                    "name": "unit",
                    "required": "required",
                    "maxlength": "10",
                }
            ),
            "unit_price": NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Unit Price",
                    "name": "unit_price",
                    "required": "required",
                    "min": 0,
                }
            ),
        }
