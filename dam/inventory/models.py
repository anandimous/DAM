from django.db import models


class ItemManager(models.Manager):
    def with_availability(self):
        quantity = models.F('quantity')
        reservations = models.Count(
            'itemreservation',
            filter=models.Q(itemreservation__is_active=True),
        )
        loans = models.Count(
            'itemloan',
            filter=models.Q(itemloan__returned_at__isnull=True),
        )
        available = quantity - reservations - loans
        return super().get_queryset().annotate(available=available)


class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to="items/")

    objects = ItemManager()

    def __str__(self):
        return self.name
