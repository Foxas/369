from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('a369.views',
    url(r'^$', 'index', name="a369-index"),
    url(r'^search/$', 'search_results', name="a369-search-results"),
)
