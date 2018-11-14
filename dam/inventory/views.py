from django.shortcuts import render, get_object_or_404
from ..inventory import models
from django.db.models import Q


def search(request):
    template = 'inventory/inventory.html'
    items = models.Item.objects.with_availability()
    args = {'items': items}

    query = request.GET.get('q')
    if query == None:
        return render(request, template, args)
    else:
        results = items.filter(Q(name__icontains = query) | Q(description__icontains = query))
        args = {
            'items':results
        }
    return render(request, template, args)

def item_details(request, item_id):
    item = get_object_or_404(models.Item, pk=item_id)
    return render(request, 'inventory/details.html', {'item_id': item.id, 'item_name': item.name, 'item_description': item.description})
