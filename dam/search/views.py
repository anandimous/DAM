from django.shortcuts import render

from dam.inventory.forms import CategoryFilterForm


def index(request):
    form = CategoryFilterForm(request.GET)
    return render(request, 'search/index.html', {'form': form})
