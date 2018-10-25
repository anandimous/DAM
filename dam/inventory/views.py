from django.shortcuts import render
from ..inventory import models


def index(request):
    items = models.Item.objects.with_availability()
    args={'items':items}
    return render(request, 'inventory/inventory.html', args)


def item_details(request, input_id):
    item_id = input_id
    item = models.Item.objects.get(pk=item_id)
    return render(request, 'inventory/details.html', {'item_id': item_id, 'item_name': item.name, 'item_description': item.description})