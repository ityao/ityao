from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^index.html', 'views.home', name='home'),
    url(r'^about.html', 'views.about', name='about'),
    url(r'^$', 'views.home', name='home'),
    (r'^time$', 'views.home'), 
    (r'^time/json$', 'views.timestamp'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^btfactory/', include('btfactory.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),  
    url(r'^accounts/', include('registration.urls')),  
    
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

