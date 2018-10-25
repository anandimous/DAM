from django.urls import path
from .views import *

app_name = 'loans'

urlpatterns = [
    path('/<int:item_id>/<str:first_name>/<str:last_name>/<str:email>',checkIfItemAvailable, name='issue')
]