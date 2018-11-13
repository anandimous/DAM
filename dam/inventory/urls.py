from django.urls import path
from .views import index, item_details, search

app_name = 'inventory'

urlpatterns = [
    path('', index, name='index'),
    path('$', search, name='search'),
    path('details/<int:item_id>', item_details, name='item-details')
]
