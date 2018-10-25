from django.urls import path
from .views import reservations,returns, allres, allrets, checkIfItemAvailable

app_name = 'loans'

urlpatterns = [
    path('reservations/<int:reservation_id>/', reservations, name='reservation'),
    path('reservations/', allres, name='allres'),
    path('loans/<int:loan_id>/', returns, name='loan'),
    path('loans/', allrets, name='allrets'),
    path('reserve/<int:item_id>/', checkIfItemAvailable, name='reserve')
]
