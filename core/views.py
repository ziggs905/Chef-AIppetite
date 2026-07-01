from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile
from mealplans.models import WeeklyPlan
from mealplans.services import plan_adherence_pct
from nutrition.services import compute_daily_targets, profile_is_complete
from progress.models import WeightEntry
from recipes.models import Recipe


@login_required
def welcome(request):
    profile = Profile.objects.filter(user=request.user).first()
    daily_targets = compute_daily_targets(profile) if profile_is_complete(profile) else None

    latest_weight = WeightEntry.objects.filter(user=request.user).order_by('-date').first()
    recent_weights = list(WeightEntry.objects.filter(user=request.user).order_by('-date')[:30])
    recent_weights.reverse()
    chart_data = {
        'labels': [entry.date.isoformat() for entry in recent_weights],
        'weights': [entry.weight_kg for entry in recent_weights],
    }

    favorite_recipes = Recipe.objects.filter(owner=request.user, is_favorite=True)[:5]

    active_plan = WeeklyPlan.objects.filter(owner=request.user).order_by('-created_at').first()
    active_plan_adherence = plan_adherence_pct(active_plan) if active_plan else None

    return render(request, 'core/welcome.html', {
        'daily_targets': daily_targets,
        'latest_weight': latest_weight,
        'chart_data': chart_data,
        'favorite_recipes': favorite_recipes,
        'active_plan': active_plan,
        'active_plan_adherence': active_plan_adherence,
    })
