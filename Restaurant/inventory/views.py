from django.shortcuts import render
from .models import Purchase, MenuItem, Ingridient, RecipeRequirement
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


def purchase(request):
    menu_items = {item.id: item.name for item in MenuItem.objects.all()}
    return render(
        request,
        "inventory/purchases.html",
        context={
            "purchases": Purchase.objects.all(),
            "menu_items": MenuItem.objects.all(),
        },
    )
