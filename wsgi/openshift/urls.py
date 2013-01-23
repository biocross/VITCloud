from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name='home'),
	url(r'^search$', 'openshift.views.search', name='search'),
    url(r'^howitworks$', 'openshift.views.pageHowitworks', name='Howitworks'),
    url(r'^topsharers$', 'openshift.views.pageTopsharers', name='Topsharers'),
    url(r'^gettheapp$', 'openshift.views.pageGettheapp', name='Gettheapp'),
    url(r'^submitone$', 'openshift.views.submitOne', name='submitOne'),\
    url(r'^interface$', 'openshift.views.interface', name='Interface'),
    url(r'^suggestions$', 'openshift.views.suggestions', name='Suggestions'),
    url(r'^file$', 'openshift.views.fileDetails', name='FileDetails'),
    url(r'^stats$', 'openshift.views.statistics', name='PerBlockStatistics'),
    


    #Uncomment this on Production. SIDS
    url(r'^purge$', 'openshift.views.clean', name='OMG DATABASE CLEANER'),
                       


    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
