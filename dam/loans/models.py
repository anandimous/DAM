from django.conf import settings
from django.db import models


class Client(models.Model):
    """A client is someone who will be reserving or checking out items."""
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def get_email_address(self):
        return self.email

    def get_full_name(self):
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
    returned_at = models.DateTimeField(null=True)  # NULL means not returned.
