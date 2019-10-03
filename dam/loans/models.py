from django.conf import settings
from django.db import models
from dam.inventory.models import Item
from datetime import datetime, timedelta
from django.utils import timezone


class ItemReservation(models.Model):
    item = models.ForeignKey('inventory.Item', models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    reservation_ends = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def get_duration(self):
        return timezone.now() + timezone.timedelta(days=14)


class ItemLoan(models.Model):
    item = models.ForeignKey('inventory.Item', models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='loans')
    approved_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='loans_approved')
    due_on = models.DateTimeField(null=True)
    returned_at = models.DateTimeField(null=True)  # NULL means not returned.

    def get_duration(self):
        return timezone.now() + timezone.timedelta(days=14)
