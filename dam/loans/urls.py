from django.urls import path

from . import views


app_name = 'loans'

urlpatterns = [
    path('reservations/<int:reservation_id>/', views.reservations, name='reservation'),
    path('reservations/', views.allres, name='allres'),
    path('loans/<int:loan_id>/', views.returns, name='loan'),
    path('loans/', views.allrets, name='allrets'),
    path('reserve/<int:item_id>/', views.reserve_item, name='reserve')
]
