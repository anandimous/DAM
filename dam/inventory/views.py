from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from dam.inventory.models import Item


def search(request):
    items = Item.objects.with_availability()
    query = request.GET.get('q')
    if query is not None:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'inventory/inventory.html', {'items': items})


def item_details(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'inventory/details.html', {'item': item})
