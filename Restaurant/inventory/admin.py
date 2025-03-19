from django.contrib import admin
from .models import Purchase, MenuItem, Ingredient, RecipeRequirement


admin.site.register(Purchase)
admin.site.register(MenuItem)
admin.site.register(Ingredient)
admin.site.register(RecipeRequirement)
# Register your models here.
