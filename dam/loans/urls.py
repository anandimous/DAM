from django.urls import path
from .views import reservations, allres, allrets

app_name = 'loans'

urlpatterns = [
    path('<int:reservation_id>/', reservations, name='reservations'),
    path('loans', allres, name='allres'),
    path('returns', allrets, name='allrets'),
]   path('',checkIfItemAvailable, name='issue')
]
