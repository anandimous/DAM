from django.urls import path
from .views import item_details, search

app_name = 'inventory'

urlpatterns = [
    path('', search, name='search'),
    path('details/<int:item_id>', item_details, name='item-details'),
]
