from django.shortcuts import render
from ..inventory import models
# Create your views here.

def index(request):
    items = models.Item.objects.all()
    args={'items':items}
    return render(request, 'inventory/inventory.html', args)


