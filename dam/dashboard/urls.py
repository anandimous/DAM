from django.conf.urls import url
from .views import showDash
from ..inventory.views import *
urlpatterns = [
    url(r'^$', showDash, name='showDash'),
]