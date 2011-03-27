from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

def design_url(regex, template, context, name):
    return url(regex, direct_to_template,
               name=name,
               kwargs={'template': template,
                       'extra_context': context})

urlpatterns = patterns('django.views.generic.simple',
    design_url(r'^$', 'index.html', {}, 'a369-index'),
    design_url(r'^search/$', 'search_results.html', {}, name="a369-search-results"),
    design_url(r'^search/json/$', 'search_results_json', {}, name="a369-json-search-results"),
)
