from django.conf import settings
from django.db import models
from datetime import datetime, timedelta, timezone

class Client(models.Model):
    """A client is someone who will be reserving or checking out items."""
    email = models.EmailField(max_length=255, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey('users.User', models.CASCADE, blank=True, null=True)

    def get_email_address(self):
        if self.user:
            return self.user.email
        return self.email

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        return '{} {}'.format(self.first_name, self.last_name)


class ItemReservation(models.Model):
    item = models.ForeignKey('inventory.Item', models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class ItemLoan(models.Model):
    item = models.ForeignKey('inventory.Item', models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    approved_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    due_on = models.DateTimeField(datetime.utcnow() + item.loan_duration)

    returned_at = models.DateTimeField(null=True)  # NULL means not returned.
