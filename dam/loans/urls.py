from django.urls import path
from .views import *

app_name = 'loans'

urlpatterns = [
    path('',checkIfItemAvailable, name='issue')
]