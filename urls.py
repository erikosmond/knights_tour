from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erikosmond.views.home', name='home'),
    # url(r'^erikosmond/', include('erikosmond.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/', index, name="index"),
)
