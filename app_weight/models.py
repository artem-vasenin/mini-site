from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models

class Weight(models.Model):
    class Meta:
        db_table = 'weight'
        ordering = ['-created_at']

    morning=models.FloatField(null=True, blank=True)
    evening=models.FloatField(null=True, blank=True)
    comment=models.CharField(max_length=255, null=True, blank=True)
    date=models.DateField(default=timezone.now)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='weights')

    def __str__(self):
        return f'{self.date}: m-{self.morning}, e-{self.evening}'
