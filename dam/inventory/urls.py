from django.urls import path
from .views import index, item_details

app_name = 'inventory'

urlpatterns = [
    path('', index, name='index'),
    path('details/<int:item_id>', item_details, name='item-details')
]
