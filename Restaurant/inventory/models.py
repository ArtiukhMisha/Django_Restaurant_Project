from django.db import models


# Create your models here.
class Ingridient(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=10)
    unit_price = models.FloatField(null=False, blank=False)

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.name


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingridients_quantity = models.JSONField(default=dict)

    def __str__(self):
        return self.menu_item.name


class Purchase(models.Model):
    menu_items = models.JSONField(default=list)
    cost = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure menu_items is a list of item IDs
        if isinstance(self.menu_items, list):
            # Fetch menu item prices from the database
            self.cost = sum(
                MenuItem.objects.filter(id__in=self.menu_items).values_list(
                    "price", flat=True
                )
            )
        else:
            self.cost = 0  # Fallback in case of incorrect data
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase on {self.timestamp} costing {self.cost}"
