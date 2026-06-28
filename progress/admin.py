from django.contrib import admin

from .models import WeightEntry


@admin.register(WeightEntry)
class WeightEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'weight_kg']
