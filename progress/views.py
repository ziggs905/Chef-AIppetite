from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from mealplans.models import WeeklyPlan
from mealplans.services import plan_adherence_pct

from .forms import WeightEntryForm
from .models import WeightEntry
from .services import apply_weight_update


@login_required
def weight_list(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save()
            apply_weight_update(entry)
            return redirect('weight_list')
    else:
        form = WeightEntryForm(user=request.user)

    entries = WeightEntry.objects.filter(user=request.user)
    chart_data = {
        'labels': [entry.date.isoformat() for entry in entries],
        'weights': [entry.weight_kg for entry in entries],
    }

    plans = WeeklyPlan.objects.filter(owner=request.user).order_by('-created_at')
    plan_adherence = [
        {'plan': plan, 'adherence_pct': plan_adherence_pct(plan)}
        for plan in plans
    ]

    return render(request, 'progress/weight_list.html', {
        'form': form,
        'entries': entries,
        'chart_data': chart_data,
        'plan_adherence': plan_adherence,
    })
