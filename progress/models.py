from django.contrib.auth.models import User
from django.db import models


class WeightEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_entries')
    date = models.DateField()
    weight_kg = models.FloatField()

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['date']

    def __str__(self):
        return f'{self.user.username} — {self.date}: {self.weight_kg}kg'
