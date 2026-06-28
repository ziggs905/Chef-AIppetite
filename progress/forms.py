from django import forms

from .models import WeightEntry


class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['date', 'weight_kg']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.instance.user = user

    def clean_date(self):
        date = self.cleaned_data['date']
        if self.user and WeightEntry.objects.filter(user=self.user, date=date).exists():
            raise forms.ValidationError('You already have a weight entry for this date.')
        return date
