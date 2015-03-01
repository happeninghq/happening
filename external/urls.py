""" External urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('external.views',
                       url(r'^$', 'index', name='index'),
                       )
