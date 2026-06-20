from django import forms

from accounts.models import Profile


class BMIForm(forms.Form):
    weight_kg = forms.FloatField(min_value=1)
    height_cm = forms.FloatField(min_value=1)


class TDEEForm(forms.Form):
    weight_kg = forms.FloatField(min_value=1)
    height_cm = forms.FloatField(min_value=1)
    age = forms.IntegerField(min_value=1)
    sex = forms.ChoiceField(choices=Profile.Sex.choices)
    activity_level = forms.ChoiceField(choices=Profile.ActivityLevel.choices)


class MacroForm(forms.Form):
    weight_kg = forms.FloatField(min_value=1)
    height_cm = forms.FloatField(min_value=1)
    age = forms.IntegerField(min_value=1)
    sex = forms.ChoiceField(choices=Profile.Sex.choices)
    activity_level = forms.ChoiceField(choices=Profile.ActivityLevel.choices)
    goal = forms.ChoiceField(choices=Profile.Goal.choices)
