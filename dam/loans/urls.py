from django.urls import path
from .views import reservations
urlpatterns = [
    path('<int:reservation_id>/', reservations, name='reservations'),
]
