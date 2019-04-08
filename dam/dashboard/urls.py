from .views import showDash
from django.urls import path

urlpatterns = [
    path('', showDash, name='showDash'),
]
