from django.urls import path
from .views import reservations, allRes
urlpatterns = [
    path('reservations/<int:reservation_id>/', reservations, name='reservations'),
    path('', allRes, name='allres')
]
