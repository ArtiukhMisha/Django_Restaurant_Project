from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("inventory/", views.inventory, name="inventory"),
    path("menu/", views.menu, name="menu"),
    path("purchases/", views.purchase, name="purchases"),
]
