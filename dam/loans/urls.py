from django.urls import path
from .views import reservations, allres


app_name = 'loans'

urlpatterns = [
    path('<int:reservation_id>/', reservations, name='reservations'),
    path('loanslist', allres, name='allres')

]
