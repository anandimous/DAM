from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from dam.inventory.models import Item
from dam.inventory.forms import CategoryFilterForm


def search(request):
    form = CategoryFilterForm(request.GET)

    items = Item.objects.with_availability()

    if form.is_valid():
        categories = form.cleaned_data['categories']
        if categories:
            items = items.filter(category__in=categories)

        query = form.cleaned_data['query']
        if query:
            items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'inventory/inventory.html', {'items': items, 'form': form})


def item_details(request, item_id):
    item = get_object_or_404(Item.objects.with_availability(), pk=item_id)
    return render(request, 'inventory/details.html', {'item': item})


def get_all_items(request):
    items = Item.objects.with_availability()
    return render(request, 'inventory/inventory_table.html', {'items': items})