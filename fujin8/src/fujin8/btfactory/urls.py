from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'fujin8.btfactory.views.index'),
    (r'^daily/$', 'fujin8.btfactory.views.daily'),
    (r'^actress/$', 'fujin8.btfactory.views.actress'),
    (r'^actress/(?P<actress_id>\d+)/$', 'fujin8.btfactory.views.actressinfo'),    
)

