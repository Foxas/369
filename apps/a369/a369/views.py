import datetime

from django.shortcuts import render_to_response
from djangosphinx.apis.current import SPHINX_API_VERSION

from haystack.views import SearchView
from haystack.query import SearchQuerySet
from haystack.forms import SearchForm


def index(self):
    kintamasis = SPHINX_API_VERSION
    return render_to_response('index.html', {'variable': kintamasis})


def search_results(request):
    sqs = SearchQuerySet()
    sqs = _add_filters(request, sqs)
    response = SearchView(template='search_results.html',\
                           form_class=SearchForm,\
                           searchqueryset=sqs).__call__(request)
    return response


def _add_filters(request, sqs):
    date_filter = None
    try:
        date_filter = request.GET['t']
    except:
        pass
    if date_filter:
        if date_filter == 'day':
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
            sqs = sqs.filter(date_birt__gte=start_date)
        elif request.GET['t']=='week':
            start_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
            sqs = sqs.filter(date_birt__gte=start_date)
        elif request.GET['t']=='month':
            start_date = datetime.datetime.now() - datetime.timedelta(days=30)
            sqs = sqs.filter(date_birt__gte=start_date)
        elif request.GET['t']=='year':
            start_date = datetime.datetime.now() - datetime.timedelta(days=356)
            sqs = sqs.filter(date_birt__gte=start_date)
        else:
            pass
    return sqs
