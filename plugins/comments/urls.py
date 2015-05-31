"""Comments urls."""

from django.conf.urls import url, include
from plugins.comments import views

urlpatterns = [
    # Overriding comments posted redirect
    url(r'^comments/posted/$', views.comment_posted),
    url(r'^comments/', include('django_comments.urls')),
]
