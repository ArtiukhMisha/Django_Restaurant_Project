from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import Purchase, MenuItem, Ingredient, RecipeRequirement
from .forms import MenuForm, ItemForm
from time import sleep
import json
import sys
from django.shortcuts import get_object_or_404
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

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
    menu_items = {i.id: i.name for i in MenuItem.objects.all()}

    return render(
        request,
        "inventory/purchases.html",
        context={
            "purchases": Purchase.objects.all(),
            "menu_items": menu_items,
        },
    )


@login_required
def create_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("inventory")
    else:
        form = ItemForm()

    context = {"form": ItemForm()}
    return render(request, "inventory/create_item.html", context)


@login_required
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


@login_required
def create_purchase(request):
    if request.method == "POST":
        selected_ingredients = request.POST.get("selected_ingredients", "").split(",")
        items = {}
        costs = []
        for item in selected_ingredients:
            if item:
                dish_id, quantity = item.split(":")
                items[dish_id] = quantity
                reqiuerments = RecipeRequirement.objects.filter(menu_item=dish_id)
                for req in reqiuerments:
                    for (
                        ingredient_id,
                        ingredient_quantity,
                    ) in req.ingredients_quantity.items():
                        logger.debug(f"Ingredient: {ingredient_id}")
                        logger.debug(f"Ingredient quantity: {ingredient_quantity}")
                        ingredient = Ingredient.objects.get(id=ingredient_id)
                        if (
                            float(ingredient_quantity) * int(quantity)
                            < ingredient.quantity
                        ):
                            ingredient.quantity -= float(ingredient_quantity) * int(
                                quantity
                            )
                            ingredient.save()
                        else:
                            return render(
                                request,
                                "inventory/error.html",
                                {"message": f"ERROR."},
                            )
                logger.debug(f"Items: {MenuItem.objects.all()}")
                menu_item = MenuItem.objects.get(id=dish_id)
                costs.append(float(menu_item.price) * float(quantity))

        purchase = Purchase.objects.create(menu_items=items, cost=sum(costs))
        purchase.save()
        return redirect("purchases")

    menu_max_amount = {}
    for i in MenuItem.objects.all():
        recipe = RecipeRequirement.objects.filter(menu_item=i.id).first()
        if recipe:
            logger.debug(f"Recipe: {recipe.ingredients_quantity}")
            ingredients = Ingredient.objects.filter(
                id__in=recipe.ingredients_quantity.keys()
            )
            l = []
            for ingredient in ingredients:
                l.append(
                    int(
                        ingredient.quantity
                        / float(recipe.ingredients_quantity.get(str(ingredient.id)))
                    )
                )
            menu_max_amount[i.id] = min(l)
    logger.debug(f"Menu max amount: {menu_max_amount}")
    context = {
        "menu_items": MenuItem.objects.all(),
        "menu_max_amount": json.dumps(menu_max_amount),
    }
    return render(request, "inventory/create_purchase.html", context)


@login_required  # ideas to add dialog window
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


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/create_item.html"
    success_url = reverse_lazy("inventory")
    form_class = ItemForm
