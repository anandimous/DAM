from django.urls import path
from .views import *

app_name = 'loans'

urlpatterns = [
    path('/<int:item_id>',checkIfItemAvailable, name='issue')
]