from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import Profile
from aiengine.services import generate_and_save_recipe
from nutrition.services import compute_daily_targets, profile_is_complete
from recipes.models import Recipe

from .forms import SwapRecipeForm, WeeklyPlanForm
from .models import PlanEntry, WeeklyPlan
from .services import (
    EmptyRecipeLibraryError,
    MEAL_SLOTS,
    generate_plan_entries,
    plan_adherence_pct,
    plan_slot_targets,
)

DAYS = range(7)
DAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


@login_required
def plan_list(request):
    plans = WeeklyPlan.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'mealplans/plan_list.html', {'plans': plans})


@login_required
def plan_create(request):
    profile = Profile.objects.filter(user=request.user).first()
    error = None

    if not profile_is_complete(profile):
        error = 'Complete your profile before creating a meal plan.'
        form = WeeklyPlanForm()
    elif request.method == 'POST':
        form = WeeklyPlanForm(request.POST)
        if form.is_valid():
            targets = compute_daily_targets(profile)
            plan = form.save(commit=False)
            plan.owner = request.user
            plan.target_calories = targets['calories']
            plan.target_protein_g = targets['protein_g']
            plan.target_carbs_g = targets['carbs_g']
            plan.target_fat_g = targets['fat_g']
            plan.save()
            try:
                generate_plan_entries(plan)
            except EmptyRecipeLibraryError as exc:
                plan.delete()
                error = str(exc)
            else:
                return redirect('plan_detail', pk=plan.pk)
    else:
        form = WeeklyPlanForm()

    return render(request, 'mealplans/plan_form.html', {'form': form, 'error': error})


@login_required
def plan_detail(request, pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    entries = list(plan.entries.select_related('recipe'))
    for entry in entries:
        entry.swap_form = SwapRecipeForm(instance=entry, owner=request.user, meal_slot=entry.meal_slot)

    grid = {day: {} for day in DAYS}
    day_totals = {day: 0 for day in DAYS}
    for entry in entries:
        grid[entry.day][entry.meal_slot] = entry
        day_totals[entry.day] += entry.recipe.calories

    days = [
        {
            'index': day,
            'name': DAY_NAMES[day],
            'slots': [{'meal_slot': slot, 'entry': grid[day].get(slot)} for slot in MEAL_SLOTS],
            'total': day_totals[day],
        }
        for day in DAYS
    ]

    slot_headers = [{'meal_slot': slot, 'target': plan_slot_targets(plan, slot)} for slot in MEAL_SLOTS]

    meal_groups = [
        {
            'meal_slot': slot,
            'target': plan_slot_targets(plan, slot),
            'recipes': Recipe.objects.filter(owner=request.user, meal_type=slot),
        }
        for slot in MEAL_SLOTS
    ]

    return render(request, 'mealplans/plan_detail.html', {
        'plan': plan, 'days': days, 'slot_headers': slot_headers, 'meal_groups': meal_groups,
        'adherence_pct': plan_adherence_pct(plan),
    })


@login_required
def plan_delete(request, pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    if request.method == 'POST':
        plan.delete()
        return redirect('plan_list')
    return render(request, 'mealplans/plan_confirm_delete.html', {'plan': plan})


@login_required
def plan_entry_swap(request, pk, entry_pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    entry = get_object_or_404(plan.entries, pk=entry_pk)
    if request.method == 'POST':
        form = SwapRecipeForm(request.POST, instance=entry, owner=request.user, meal_slot=entry.meal_slot)
        if form.is_valid():
            form.save()
    return redirect('plan_detail', pk=plan.pk)


@login_required
def plan_generate_slot_recipe(request, pk, meal_slot):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    if meal_slot not in MEAL_SLOTS:
        raise Http404
    if request.method == 'POST':
        profile = Profile.objects.filter(user=request.user).first()
        targets = plan_slot_targets(plan, meal_slot)
        generate_and_save_recipe(request.user, profile, targets, meal_slot)
    return redirect('plan_detail', pk=plan.pk)


@login_required
def plan_fill_entry(request, pk, day, meal_slot):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    if meal_slot not in MEAL_SLOTS or day not in DAYS:
        raise Http404
    if request.method == 'POST' and not plan.entries.filter(day=day, meal_slot=meal_slot).exists():
        profile = Profile.objects.filter(user=request.user).first()
        targets = plan_slot_targets(plan, meal_slot)
        recipe, error = generate_and_save_recipe(request.user, profile, targets, meal_slot)
        if recipe:
            PlanEntry.objects.create(plan=plan, day=day, meal_slot=meal_slot, recipe=recipe)
    return redirect('plan_detail', pk=plan.pk)


@login_required
@require_POST
def plan_entry_toggle_completed(request, pk, entry_pk):
    plan = get_object_or_404(WeeklyPlan, pk=pk, owner=request.user)
    entry = get_object_or_404(plan.entries, pk=entry_pk)
    entry.completed = not entry.completed
    entry.save(update_fields=['completed'])
    return JsonResponse({'completed': entry.completed, 'adherence_pct': plan_adherence_pct(plan)})
