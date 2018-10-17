from django.conf.urls import url
from .views import showDash
from ..results.views import *
urlpatterns = [
    url(r'^$', showDash, name='showDash'),
]