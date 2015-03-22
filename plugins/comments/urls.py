"""Comments urls."""

from django.conf.urls import patterns, include

urlpatterns = patterns('plugins.comments.views',
                       # Overriding comments posted redirect
                       (r'^comments/posted/$', 'comment_posted'),
                       (r'^comments/', include('django_comments.urls')),
                       )
