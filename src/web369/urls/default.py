from django.conf.urls.defaults import include, url, patterns, handler500, handler404
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)


urlpatterns += patterns('web369.views',
    url(r'^$', 'index', name="web369-index"),
    url(r'^search/$', 'search_results', name="web369-search-results"),
)
