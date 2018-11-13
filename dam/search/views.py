from django.shortcuts import render
from django.db.models import Q
from ..inventory import models
def index(request):
    return render(request, 'search/index.html')


def search(request):
    template = 'inventory/inventory.html'
    query = request.GET.get('q')
    results = models.ItemManager.filter(Q(name__icontains = query) | Q(description__icontains = query))
    context ={
        'items':results
    }
    return render(request, template, context)