from django.conf.urls import url
from .views import showMain
from ..inventory.views import *
urlpatterns = [
    url(r'^$', showMain, name='showMain'),
    url(r'^dam/inventory/$', index, name='index')
]