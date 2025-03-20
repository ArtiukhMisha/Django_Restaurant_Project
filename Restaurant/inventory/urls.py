from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("menu/", views.menu, name="menu"),
    path("purchases/", views.purchase, name="purchases"),
    path("recipes/", views.recipes, name="recipes"),
    path("menu/create/", views.create_menu, name="create_menu"),
    path("menu/delete/<int:id>/", views.delete, name="delete"),  # deletes all
    path("inventory/create/", views.create_item, name="create_item"),
    path("purchase/create/", views.create_purchase, name="create_purchase"),
    path(
        "inventory/<int:pk>/update", views.ItemUpdateView.as_view(), name="item_update"
    ),
]
