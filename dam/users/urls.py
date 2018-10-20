from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('log-in/', views.LogInView.as_view(), name='log-in'),
]
