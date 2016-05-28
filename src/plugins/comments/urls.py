"""Comments urls."""

from django.conf.urls import url
from plugins.comments import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/discussion$', views.event_discussion,
        name='event_discussion'),
    url(r'^new$', views.post_comment,
        name='post_comment'),
]
