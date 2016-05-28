"""Pages urls."""

from django.conf.urls import url
from pages import views

urlpatterns = [
    url(r'^(?P<pk>.+)$', views.view, name='view_page'),
]
