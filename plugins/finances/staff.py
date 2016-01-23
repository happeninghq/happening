"""Finances administration."""

from django.conf.urls import url
from plugins.finances import views


urlpatterns = [
    url(r'^account$', views.account, name='finances'),
    url(r'^create-account$', views.create_account,
        name='finances_create_account'),
    url(r'^create-transaction$', views.create_transaction,
        name='finances_create_transaction'),
]

staff_links = (
    ("Finances", "finances"),
)
