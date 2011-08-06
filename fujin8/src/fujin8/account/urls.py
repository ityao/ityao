from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('fujin8.sinaweibo.views',
    url(r'^login/$', 'login', name='log'),
    url(r'^logincheck/$', 'login_check', name='logcheck'),
    url(r'^logout/$', 'logout', name='logout'),
)

