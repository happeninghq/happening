"""External urls."""

from django.conf.urls import url
from external import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
