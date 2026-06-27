from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import Profile
from nutrition.services import DEFAULT_MEAL_RATIOS, compute_daily_targets, profile_is_complete, slot_targets

from .forms import GenerateRecipeForm
from .services import generate_and_save_recipe


@login_required
def generate_recipe(request):
    profile = Profile.objects.filter(user=request.user).first()
    daily_targets = compute_daily_targets(profile) if profile_is_complete(profile) else None
    meal_targets = None
    if daily_targets:
        meal_targets = {
            meal_type: slot_targets(daily_targets, pct)
            for meal_type, pct in DEFAULT_MEAL_RATIOS.items()
        }
    error = None
    form = GenerateRecipeForm(request.POST or None)

    if request.method == 'POST' and daily_targets and form.is_valid():
        meal_type = form.cleaned_data['meal_type']
        targets = slot_targets(daily_targets, DEFAULT_MEAL_RATIOS[meal_type])
        recipe, error = generate_and_save_recipe(
            request.user, profile, targets, meal_type, form.cleaned_data['preferences'],
        )
        if recipe:
            return redirect('recipe_detail', pk=recipe.pk)

    return render(request, 'aiengine/generate_recipe.html', {
        'form': form, 'meal_targets': meal_targets, 'error': error,
    })
