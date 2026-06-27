from django import forms

from recipes.models import Recipe

from .models import PlanEntry, WeeklyPlan

PCT_FIELDS = ['breakfast_pct', 'lunch_pct', 'dinner_pct', 'snack_pct']


class WeeklyPlanForm(forms.ModelForm):
    class Meta:
        model = WeeklyPlan
        fields = ['name', 'start_date'] + PCT_FIELDS
        widgets = {'start_date': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super().clean()
        if all(cleaned_data.get(field) is not None for field in PCT_FIELDS):
            total = sum(cleaned_data[field] for field in PCT_FIELDS)
            if total != 100:
                raise forms.ValidationError('The four percentages must add up to 100.')
        return cleaned_data


class SwapRecipeForm(forms.ModelForm):
    class Meta:
        model = PlanEntry
        fields = ['recipe']

    def __init__(self, *args, owner=None, meal_slot=None, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Recipe.objects.none()
        if owner is not None:
            queryset = Recipe.objects.filter(owner=owner)
            if meal_slot is not None:
                queryset = queryset.filter(meal_type=meal_slot)
        self.fields['recipe'].queryset = queryset
