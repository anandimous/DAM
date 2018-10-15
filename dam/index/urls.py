from django.conf.urls import url
from .views import showMain
from ..results.views import *
urlpatterns = [
    url(r'^$', showMain, name='showMain'),
    url(r'^dam/results/$', index, name='index')

]