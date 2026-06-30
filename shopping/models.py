from django.contrib.auth.models import User
from django.db import models

from mealplans.models import WeeklyPlan
from recipes.models import Ingredient


class ShoppingList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_lists')
    plan = models.ForeignKey(
        WeeklyPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='shopping_lists',
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ShoppingItem(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10, choices=Ingredient.Unit.choices)
    checked = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f'{self.quantity} {self.unit} {self.name}'
