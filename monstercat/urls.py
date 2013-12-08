import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from website.views import WebappView
from api.views import AlbumsApiView, SinglesApiView, StreamingApiView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'monstercat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^api/albums.json$', AlbumsApiView.as_view(), name='api_albums'),
    url(r'^api/singles.json$', SinglesApiView.as_view(), name='api_singles'),
    url(r'^api/streaming.json$', StreamingApiView.as_view(), name='api_streaming'),
    url(r'^$', WebappView.as_view(), name='index'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()