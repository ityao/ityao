from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'fujin8.polls.views.index'),
    (r'^(?P<poll_id>\d+)/$', 'fujin8.polls.views.detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'fujin8.polls.views.results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'fujin8.polls.views.vote'),    
)

