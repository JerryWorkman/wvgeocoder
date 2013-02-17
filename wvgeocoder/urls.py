from django.conf.urls import patterns, include, url
from views import get_site, home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'wvgeocoder.views.home', name='home'),
    # url(r'^wvgeocoder/', include('wvgeocoder.foo.urls')),
    url(r'^site/(\d+)/$', 'wvgeocoder.views.get_site', name='get_site'),
    url(r'^site/search/$', 'wvgeocoder.views.site_search_form', name='site_search'),
    url(r'^site/list/$', 'wvgeocoder.views.site_search', name='site_list'),
    url(r'^address/normalize/(.*)/$', 'wvgeocoder.views.normalize_address', name='normalize'),
    url(r'^address/geocode/map$', 'wvgeocoder.views.get_geocode_site', name='geocode_map'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()