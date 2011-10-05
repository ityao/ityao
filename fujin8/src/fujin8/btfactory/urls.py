from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

'''(r'^daily/$', 'fujin8.btfactory.views.daily', 'daily_film_auth'),'''
urlpatterns = patterns('',
    (r'^$', 'fujin8.btfactory.views.index'),
    (r'^moviethumbcron/$', 'fujin8.btfactory.views.moviethumbcron'),
    (r'^dailycron/$', 'fujin8.btfactory.views.dailycron'),
    (r'^actresscron/$', 'fujin8.btfactory.views.actresscron'),
    (r'^(?P<daily_id>\d+)/daily/$', 'fujin8.btfactory.views.dailymovie'),
    (r'^movie/(?P<movie_id>\d+)/confirm/$', 'fujin8.btfactory.views.confirmMovie'),    
    (r'^actress/$', 'fujin8.btfactory.views.actress'),
    (r'^actress/(?P<actress_id>\d+)/$', 'fujin8.btfactory.views.actressinfo'),
    url(r'^daily/$', 'fujin8.btfactory.views.daily', name='daily_film_auth'),
    url(r'^new/$', 'fujin8.btfactory.views.newfilm', name='new_film'),
)

