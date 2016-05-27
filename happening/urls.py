"""Overall URL file."""

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
import importlib
from happening.utils import plugin_enabled_decorator
from lib.required import required
from happening import views
from rest_framework import routers
from events import api as events_api
from happening import api as happening_api

# Initialise the plugins
from happening.plugins import init
from periodically import autodiscover

# There isn't a great place to put initialisation code
# so for now we'll put it in the primary urls.py
init()
autodiscover()

# from notifications import api as notifications_api

router = routers.DefaultRouter()
router.register(r'users', happening_api.UserViewSet)
router.register(r'events', events_api.EventViewSet)
router.register(r'tickettypes', events_api.TicketTypeViewSet)
router.register(r'tickets', events_api.TicketViewSet)
router.register(r'ticketorders', events_api.TicketOrderViewSet)
# router.register(r'notifications', notifications_api.NotificationViewSet)


urlpatterns = [
    url(r'^staff/', include('staff.urls')),
    url(r'^admin/', include('admin.urls')),
    url(r'^events/', include('events.urls')),

    # Include general external pages as fallback
    url(r'^', include('external.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^member/', include('members.urls')),
    url(r'^notifications/', include('notifications.urls')),
    url(r'^pages/', include('pages.urls')),
    url(r'^payments/', include('payments.urls')),

    url(r'^upload$', views.file_upload, name='file_upload'),


    url(r'^follow$', views.follow, name='follow'),
    url(r'^unfollow$', views.unfollow, name='unfollow'),

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

for plugin in settings.PLUGINS:
    p = importlib.import_module(plugin)
    if hasattr(p.Plugin, "url_root"):
        # Include the urlpatterns
        urlpatterns += required(
            plugin_enabled_decorator(plugin),
            [url(p.Plugin.url_root, include("%s.urls" % plugin))])
