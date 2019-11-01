import csv
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
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


@permission_required('loans.change_itemloan')
def get_all_items(request):
    items = Item.objects.with_availability()
    return render(request, 'inventory/inventory_table.html', {'items': items})


def get_inventory_status_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory_status.csv"'
    # Get all items in inventory
    items = Item.objects.with_availability()

    writer = csv.writer(response)
    writer.writerow([
        'Inventory',
        'Item',
        'ID',
        'Category',
        'Status',
        'Pending Reservation',
        'Loaned On',
        'Loaned To',
        'Due On'
    ])

    for item in items:
        writer.writerow([
            item.inventory.name,
            item.name,
            item.item_id,
            item.category,
            'Available' if item.available > 0 else 'Unavailable',
            'Yes' if item.active_reservation else 'No',
            item.active_loan.approved_at if item.active_loan else 'N/A',
            item.active_loan.user.get_full_name if item.active_loan else 'N/A',
            item.active_loan.due_on if item.active_loan else 'N/A'
        ])

    return response
