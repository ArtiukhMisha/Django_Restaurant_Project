from django.shortcuts import render, redirect
from .models import Purchase, MenuItem, Ingridient, RecipeRequirement
from .forms import MenuForm, RecipeRequirementForm, RecipeRequirementForm
# Create your views here.


def home(request):
    return render(request, "inventory/home.html")


def inventory(request):
    return render(
        request,
        "inventory/inventory.html",
        context={"ingridients": Ingridient.objects.all()},
    )


def menu(request):
    return render(
        request,
        "inventory/menu.html",
        context={"menu_items": MenuItem.objects.all()},
    )


def recipes(request):
    ingridients = {i.id: i.name for i in Ingridient.objects.all()}
    return render(
        request,
        "inventory/recipes.html",
        context={
            "ingridients": ingridients,
            "recipes": RecipeRequirement.objects.all(),
        },
    )


def purchase(request):
    return render(
        request,
        "inventory/purchases.html",
        context={
            "purchases": Purchase.objects.all(),
            "menu_items": MenuItem.objects.all(),
        },
    )


def create_menu(request):
    menu_form = MenuForm()
    recipe_form = RecipeRequirementForm()

    context = {
        "inventory": Ingridient.objects.all(),
        "menu_form": menu_form,
        "recipe_form": recipe_form,
    }
    return render(request, "inventory/create_menu.html", context)
