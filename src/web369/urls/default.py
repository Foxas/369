from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('web369.views',
    url(r'^$', 'index', name="web369-index"),
    url(r'^search/$', 'search_results', name="web369-search-results"),
)
