from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.models import Profile

from .calculations import (
    calculate_bmi,
    calculate_bmr,
    calculate_goal_calories,
    calculate_macros,
    calculate_tdee,
    get_bmi_category,
)
from .forms import BMIForm, MacroForm, TDEEForm

BMI_INTERPRETATIONS = {
    'underweight': 'This is below the healthy range; consider a calorie surplus.',
    'normal': 'This is within the healthy weight range.',
    'overweight': 'This is above the healthy range; a modest calorie deficit may help.',
    'obese': 'This is well above the healthy range; consider talking to a healthcare professional.',
}


def _profile_initial(profile, fields):
    if profile is None:
        return {}
    return {field: getattr(profile, field) for field in fields if getattr(profile, field)}


@login_required
def bmi_calculator(request):
    profile = Profile.objects.filter(user=request.user).first()
    result = None
    if request.method == 'POST':
        form = BMIForm(request.POST)
        if form.is_valid():
            bmi = calculate_bmi(form.cleaned_data['weight_kg'], form.cleaned_data['height_cm'])
            category = get_bmi_category(bmi)
            result = {
                'bmi': round(bmi, 1),
                'category': category,
                'interpretation': BMI_INTERPRETATIONS[category],
            }
    else:
        form = BMIForm(initial=_profile_initial(profile, ['weight_kg', 'height_cm']))
    return render(request, 'nutrition/bmi_calculator.html', {'form': form, 'result': result})


@login_required
def tdee_calculator(request):
    profile = Profile.objects.filter(user=request.user).first()
    result = None
    if request.method == 'POST':
        form = TDEEForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bmr = calculate_bmr(data['weight_kg'], data['height_cm'], data['age'], data['sex'])
            tdee = calculate_tdee(bmr, data['activity_level'])
            result = {'bmr': round(bmr), 'tdee': round(tdee)}
    else:
        fields = ['weight_kg', 'height_cm', 'age', 'sex', 'activity_level']
        form = TDEEForm(initial=_profile_initial(profile, fields))
    return render(request, 'nutrition/tdee_calculator.html', {'form': form, 'result': result})


@login_required
def macro_calculator(request):
    profile = Profile.objects.filter(user=request.user).first()
    result = None
    if request.method == 'POST':
        form = MacroForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            bmr = calculate_bmr(data['weight_kg'], data['height_cm'], data['age'], data['sex'])
            tdee = calculate_tdee(bmr, data['activity_level'])
            goal_calories = calculate_goal_calories(tdee, data['goal'])
            macros = calculate_macros(goal_calories, data['goal'])
            result = {
                'goal_calories': round(goal_calories),
                'protein_g': round(macros['protein_g']),
                'carbs_g': round(macros['carbs_g']),
                'fat_g': round(macros['fat_g']),
            }
    else:
        fields = ['weight_kg', 'height_cm', 'age', 'sex', 'activity_level', 'goal']
        form = MacroForm(initial=_profile_initial(profile, fields))
    return render(request, 'nutrition/macro_calculator.html', {'form': form, 'result': result})
