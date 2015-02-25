""" Notification urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('notifications.views',
                       url(r'^list$', 'list',
                           name='notifications_list'),
                       url(r'^short$', 'short',
                           name='notifications_short'),
                       url(r'^settings$', 'settings',
                           name='notifications_settings'),
                       )
