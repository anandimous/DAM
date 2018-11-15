from django.urls import path

from . import views


app_name = 'users'

urlpatterns = [
    path('create-account/', views.CreateAccountView.as_view(), name='create-account'),
    path('log-in/', views.LogInView.as_view(), name='log-in'),
    path('log-out/', views.LogOutView.as_view(), name='log-out'),
]
