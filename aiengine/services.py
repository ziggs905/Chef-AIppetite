from recipes.models import Ingredient, Recipe, Tag

from .parsing import RecipeParseError, parse_recipe
from .prompts import build_recipe_prompt
from .providers import get_provider


def generate_and_save_recipe(user, profile, targets, meal_type, preferences=''):
    """Build a prompt, call the AI provider, parse the result, and save a Recipe.

    Returns (recipe, error) — exactly one of the two is set.
    """
    prompt = build_recipe_prompt(profile, targets, preferences, meal_type=meal_type)
    raw_json = get_provider().generate_recipe(prompt)
    try:
        data = parse_recipe(raw_json)
    except RecipeParseError as exc:
        return None, str(exc)

    recipe = Recipe.objects.create(
        owner=user,
        title=data['title'],
        description=data['description'],
        meal_type=meal_type,
        servings=data['servings'],
        prep_minutes=data['prep_minutes'],
        cook_minutes=data['cook_minutes'],
        calories=data['calories'],
        protein_g=data['protein_g'],
        carbs_g=data['carbs_g'],
        fat_g=data['fat_g'],
        steps=data['steps'],
        source=Recipe.Source.AI,
    )
    Ingredient.objects.bulk_create(
        Ingredient(recipe=recipe, **item) for item in data['ingredients']
    )
    if data['tags']:
        recipe.tags.set(Tag.objects.filter(slug__in=data['tags']))
    return recipe, None
