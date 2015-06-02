"""Membership urls."""

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^membership$', views.my_membership, name='my_membership'),
    url(r'^(?P<pk>\d+)/membership$', views.membership, name='membership'),
    url(r'^membership/(?P<pk>\d+)/payment/$', views.membership_payment_success,
        name='membership_payment_success'),
    url(r'^membership/(?P<pk>\d+)/payment/fail$',
        views.membership_payment_failure,
        name='membership_payment_failure'),
]
