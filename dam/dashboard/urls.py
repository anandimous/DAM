from django.conf.urls import url
from .views import showDash

urlpatterns = [
    url(r'^$', showDash, name='showDash'),
]