from django.contrib import admin

from .models import ShoppingItem, ShoppingList


class ShoppingItemInline(admin.TabularInline):
    model = ShoppingItem
    extra = 0


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'plan', 'created_at']
    inlines = [ShoppingItemInline]


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ['shopping_list', 'name', 'quantity', 'unit', 'checked']
