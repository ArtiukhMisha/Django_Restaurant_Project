from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=10)
    unit_price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.id) + " " + self.name


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredients_quantity = models.JSONField()

    def __str__(self):
        return self.menu_item.name


class Purchase(models.Model):
    menu_items = models.JSONField()
    cost = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure menu_items is a dictionary of item IDs and quantities
        if isinstance(self.menu_items, dict):
            self.cost = sum(
                float(MenuItem.objects.get(id=item_id).price) * float(quantity)
                for item_id, quantity in self.menu_items.items()
            )
        else:
            self.cost = 0  # Fallback in case of incorrect data
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase on {self.timestamp} costing {self.cost}"
