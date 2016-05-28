"""Payment urls."""

from django.conf.urls import url
from payments import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/pay$', views.make_payment, name='make_payment'),
]
