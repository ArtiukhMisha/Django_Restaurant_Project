from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from .models import Purchase, MenuItem, Ingredient, RecipeRequirement
from .forms import MenuForm
from time import sleep
import sys
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("formatted.log")
stream_handler = logging.StreamHandler(sys.stdout)
formatter2 = logging.Formatter("[%(asctime)s] {%(levelname)s} - %(message)s")
stream_handler.setFormatter(formatter2)
file_handler.setFormatter(formatter2)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def home(request):
    return render(request, "inventory/home.html")


def inventory(request):
    return render(
        request,
        "inventory/inventory.html",
        context={"ingredients": Ingredient.objects.all()},
    )


def menu(request):
    return render(
        request,
        "inventory/menu.html",
        context={"menu_items": MenuItem.objects.all()},
    )


def recipes(request):
    ingredients = {i.id: i.name for i in Ingredient.objects.all()}
    logger.debug(f"Ingredients: {ingredients}")
    return render(
        request,
        "inventory/recipes.html",
        context={
            "ingredients": ingredients,
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
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu_item = form.save()
            selected_ingredients = request.POST.get("selected_ingredients", "").split(
                ","
            )
            ingredients = {}
            for item in selected_ingredients:
                if item:
                    ingredient_id, quantity = item.split(":")
                    ingredients[ingredient_id] = quantity
            logger.debug(f"Ingredients: {ingredients}")
            recipe = RecipeRequirement.objects.create(
                menu_item=menu_item, ingredients_quantity=ingredients
            )
            recipe.save()
            return redirect("menu")
    else:
        form = MenuForm()

    context = {
        "inventory": Ingredient.objects.all(),
        "menu_form": form,
    }
    return render(request, "inventory/create_menu.html", context)


# ideas to add dialog window
def delete(request, id):
    model_name = request.GET.get("model")
    model_class = {
        "menu": MenuItem,
        "inventory": Ingredient,
        "recipes": RecipeRequirement,
        "purchases": Purchase,
    }.get(model_name.lower())
    if model_class:
        item = get_object_or_404(model_class, id=id)
        item.delete()
    return redirect(model_name)
