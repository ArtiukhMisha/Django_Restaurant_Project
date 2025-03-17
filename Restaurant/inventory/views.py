from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "inventory/home.html")


def inventory(request):
    return render(request, "inventory/inventory.html")


def menu(request):
    return render(request, "inventory/menu.html")


def purchase(request):
    return render(request, "inventory/purchases.html")
