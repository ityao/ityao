from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

'''(r'^daily/$', 'btfactory.views.daily', 'daily_film_auth'),'''
urlpatterns = patterns('fujin8.btfactory.views',
    (r'^$', 'index'),
    (r'^moviethumbcron/$', 'moviethumbcron'),
    (r'^dailycron/$', 'dailycron'),
    (r'^actresscron/$', 'actresscron'),
    (r'^(?P<daily_id>\d+)/daily/$', 'dailymovie'),
    (r'^movie/(?P<movie_id>\d+)/confirm/$', 'confirmMovie'),    
    (r'^actress/$', 'actress'),
    (r'^actress/(?P<actress_id>\d+)/$', 'actressinfo'),
    url(r'^daily/$', 'daily', name='daily_film_auth'),
    url(r'^new/$', 'newfilm', name='new_film'),
)

