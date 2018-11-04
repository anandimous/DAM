from django.shortcuts import render, get_object_or_404
from ..inventory import models


def index(request):
    items = models.Item.objects.with_availability()
    args={'items': items}
    return render(request, 'inventory/inventory.html', args)


def item_details(request, item_id):
    item = get_object_or_404(models.Item, pk=item_id)
    return render(request, 'inventory/details.html', {'item_id': item.id, 'item_name': item.name, 'item_description': item.description})
