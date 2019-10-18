from django.urls import path
from .views import item_details, search, get_all_items

app_name = 'inventory'

urlpatterns = [
    path('', search, name='search'),
    path('details/<int:item_id>/', item_details, name='item-details'),
    path('list', get_all_items, name='inventory-list')
]
