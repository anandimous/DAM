from django.db import models
from django.utils import timezone


class Inventory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'inventories'

    def __str__(self):
        return self.name


class ItemManager(models.Manager):
    def with_availability(self):
        quantity = models.F('quantity')
        reservations = models.Count(
            'itemreservation',
            distinct=True,
            filter=models.Q(itemreservation__is_active=True),
        )
        loans = models.Count(
            'itemloan',
            distinct=True,
            filter=models.Q(itemloan__returned_at__isnull=True),
        )
        available = quantity - reservations - loans
        return super().get_queryset().annotate(available=available)


class Item(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    loan_duration = models.DurationField(default=timezone.timedelta(days=14))
    image = models.ImageField(upload_to="items", default="items/placeholder.png")
    item_id = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=100, null=True)
    metadata = models.TextField(null=True)

    objects = ItemManager()

    def __str__(self):
        return self.name + ' : ' + self.item_id


class Category(models.Model):
    name = models.CharField(max_length=100)
    items = models.ManyToManyField(Item, blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'categories'
