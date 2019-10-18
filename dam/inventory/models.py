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
        available = 1 - reservations - loans
        return super().get_queryset().annotate(available=available)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name_plural = 'categories'


class Item(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    loan_duration = models.DurationField(default=timezone.timedelta(days=14))
    image = models.ImageField(upload_to="items", default="items/placeholder.png")
    item_id = models.CharField(max_length=50, blank=True)
    serial_number = models.CharField(max_length=100, blank=True)
    metadata = models.TextField(blank=True)

    objects = ItemManager()

    @property
    def active_reservation(self):
        reservations = Item.objects.get(pk=self.pk).itemreservation_set.filter(is_active=True)
        return reservations[0] if reservations else None

    @property
    def active_loan(self):
        loans = Item.objects.get(pk=self.pk).itemloan_set.filter(returned_at__isnull=True)
        return loans[0] if loans else None

    def __str__(self):
        return self.name + ' : ' + self.item_id