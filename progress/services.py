from datetime import date

from .models import WeightEntry


def apply_weight_update(entry):
    """Update the owning Profile's weight_kg if this entry is today's or the latest known."""
    is_latest = not WeightEntry.objects.filter(
        user=entry.user, date__gt=entry.date
    ).exclude(pk=entry.pk).exists()
    if entry.date == date.today() or is_latest:
        profile = entry.user.profile
        profile.weight_kg = entry.weight_kg
        profile.save(update_fields=['weight_kg'])
