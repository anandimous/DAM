from django.db import models


class Client(models.Model):
    """A client is someone who will be reserving or checking out items."""
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class ItemReservation(models.Model):
    item = models.ForeignKey('inventory.Item', models.CASCADE)
    client = models.ForeignKey(Client, models.CASCADE)
    reserved_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
