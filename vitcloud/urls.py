from django.conf.urls import patterns, include, url
from django.contrib import admin

from vitcloud.views import *

admin.autodiscover()

urlpatterns = patterns('',
   	url(r'^$', 'vitcloud.views.home', name='home'),
	url(r'^search$', 'vitcloud.views.search', name='search'),
    url(r'^howitworks$', 'vitcloud.views.pageHowitworks', name='Howitworks'),
    url(r'^topsharers$', 'vitcloud.views.pageTopsharers', name='Topsharers'),
    url(r'^gettheapp$', 'vitcloud.views.pageGettheapp', name='Gettheapp'),
    url(r'^interface$', 'vitcloud.views.interface', name='Interface'),
    url(r'^suggestions$', 'vitcloud.views.suggestions', name='Suggestions'),
    url(r'^file$', 'vitcloud.views.fileDetails', name='FileDetails'),
    url(r'^stats$', 'vitcloud.views.statistics', name='PerBlockStatistics'),
    url(r'^apifeed$', 'vitcloud.views.apiFeed', name='ApiFeed'),
    


    #Uncomment this on Production. SIDS
    url(r'^purge$', 'vitcloud.views.clean', name='OMG DATABASE CLEANER'),
    url(r'^submitone$', 'vitcloud.views.submitOne', name='submitOne'),

    url(r'^admin/', include(admin.site.urls)),
)



