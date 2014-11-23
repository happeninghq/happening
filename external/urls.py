""" External urls. """

from django.conf.urls import patterns, url

urlpatterns = patterns('external.views',
                       url(r'^$', 'index', name='index'),
                       url(r'^sponsorship$', 'sponsorship',
                           name='sponsorship'),

                       # These are temporary URLs until events are
                       # stored in the database
                       url(r'^report_1$', 'report_1', name='report_1'),
                       url(r'^report_2$', 'report_2', name='report_2'),
                       url(r'^report_3$', 'report_3', name='report_3'),
                       url(r'^report_4$', 'report_4', name='report_4'),
                       url(r'^report_5$', 'report_5', name='report_5'),
                       url(r'^report_6$', 'report_6', name='report_6'),
                       url(r'^report_7$', 'report_7', name='report_7'),
                       url(r'^report_8$', 'report_8', name='report_8'),
                       )
