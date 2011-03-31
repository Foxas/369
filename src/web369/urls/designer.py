from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.core.paginator import Paginator
import datetime
import lipsum

def _url(regex, template, context, name):
    return url(regex, direct_to_template,
               name=name,
               kwargs={'template': template,
                       'extra_context': context})

g = lipsum.Generator()

results = [
    {'item_link': 'http://www.google.com',
     'author': g.generate_sentence().split(' ')[0].title(),
     'subject_title': '%s' % g.generate_sentence(),
     'date': datetime.datetime(2011, i % 12 + 1, i % 27 + 1),
     'content': g.generate_paragraph(),}
    for i in range(1, 10)
]

search_results = {
    'results': results,
    'pages': {'num_pages': 5},
    'page': Paginator(range(1, 50), 10).page(2),
}

urlpatterns = patterns('django.views.generic.simple',
    _url(r'^$', 'index.html', {}, 'web369-index'),
    _url(r'^search/$', 'search_results.html', search_results, 
         name="web369-search-results"),
)
