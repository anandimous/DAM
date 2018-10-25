from django.urls import path
from .views import *

app_name = 'inventory'

urlpatterns = [
    path('', index, name='index'),
    path('details/<int:input_id>', item_details, name='item-details')
]
