from django.urls import path
from .views import checkIfItemAvailable

app_name = 'loans'

urlpatterns = [
    path('/reserve/<int:item_id>/',checkIfItemAvailable, name='reserve')
]
