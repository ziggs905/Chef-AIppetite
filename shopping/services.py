from mealplans.models import PlanEntry

from .models import ShoppingItem, ShoppingList


def generate_shopping_list(owner, plan, name):
    """Aggregate a plan's recipe ingredients by (name.lower(), unit) into a new ShoppingList."""
    aggregated = {}
    entries = PlanEntry.objects.filter(plan=plan).select_related('recipe').prefetch_related('recipe__ingredients')
    for entry in entries:
        for ingredient in entry.recipe.ingredients.all():
            key = (ingredient.name.lower(), ingredient.unit)
            aggregated[key] = aggregated.get(key, 0) + ingredient.quantity

    shopping_list = ShoppingList.objects.create(owner=owner, plan=plan, name=name)
    items = [
        ShoppingItem(shopping_list=shopping_list, name=item_name, quantity=quantity, unit=unit, position=position)
        for position, ((item_name, unit), quantity) in enumerate(sorted(aggregated.items()))
    ]
    ShoppingItem.objects.bulk_create(items)
    return shopping_list
