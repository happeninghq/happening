"""Pages urls."""

from django.conf.urls import patterns, url

urlpatterns = patterns('pages.views',
                       url(r'^(?P<pk>.+)$', 'view',
                           name='view_page'),
                       )
