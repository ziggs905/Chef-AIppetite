from recipes.models import Recipe

from .models import PlanEntry

DAYS = range(7)
MEAL_SLOTS = ['breakfast', 'lunch', 'dinner', 'snack']


class EmptyRecipeLibraryError(Exception):
    pass


def generate_plan_entries(plan):
    """Fill a WeeklyPlan's 7x4 grid, matching each slot to a recipe of that meal_type.

    A slot is left empty (no entry) if the owner has no recipes of that meal_type.
    """
    recipes_by_slot = {
        slot: list(Recipe.objects.filter(owner=plan.owner, meal_type=slot))
        for slot in MEAL_SLOTS
    }
    if not any(recipes_by_slot.values()):
        raise EmptyRecipeLibraryError('Generate some recipes first, then create a plan.')

    entries = []
    for day in DAYS:
        used_today = set()
        for slot in MEAL_SLOTS:
            candidates_all = recipes_by_slot[slot]
            if not candidates_all:
                continue
            candidates = [r for r in candidates_all if r.pk not in used_today] or candidates_all
            slot_target = plan.target_calories * getattr(plan, f'{slot}_pct') / 100
            recipe = min(candidates, key=lambda r: abs(r.calories - slot_target))
            used_today.add(recipe.pk)
            entries.append(PlanEntry(plan=plan, day=day, meal_slot=slot, recipe=recipe))

    PlanEntry.objects.bulk_create(entries)


def plan_slot_targets(plan, meal_slot):
    """This plan's own calorie/macro budget for one meal slot, using its own ratios."""
    fraction = getattr(plan, f'{meal_slot}_pct') / 100
    return {
        'calories': round(plan.target_calories * fraction),
        'protein_g': round(plan.target_protein_g * fraction, 1),
        'carbs_g': round(plan.target_carbs_g * fraction, 1),
        'fat_g': round(plan.target_fat_g * fraction, 1),
    }


def plan_adherence_pct(plan):
    total = plan.entries.count()
    if total == 0:
        return 0
    completed = plan.entries.filter(completed=True).count()
    return round(completed / total * 100)
