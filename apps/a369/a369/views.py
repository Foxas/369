from djangosphinx.apis.current import SPHINX_API_VERSION
from django.core.paginator import Paginator
from django.template.loader import get_template

from annoying.decorators import render_to, ajax_request

from .models import CommentItem


@render_to('index.html')
def index(request):
    kintamasis = SPHINX_API_VERSION
    return {'variable': kintamasis}


@render_to('search_results.html')
def search_results(request):
    query = request.GET.get('q')
    if not query:
        return {'TEMPLATE': 'search_no_results.html'}
    results = CommentItem.search.query(query)
    pages = Paginator(results, 10)
    return {
        'results': results,
        'pages': pages,
        'page': pages.page(request.GET.get('page', 1)),
        'query': query,
    }

@ajax_request
def search_results_json(request):
    query = request.GET.get('q')
    results = CommentItem.search.query(query)
    pages = Paginator(results, 10)
    page = pages.page(request.GET.get('page', 1))
    t = get_template('search_r_item.html')
    for result in results:
        out += t.render(Context({'result': result}))

    return {
        'hasNext': page.has_next(),
        'itemsHtml': 'foo',
        'results': results,
        'pages': pages,
        'page': page,
        'query': query,
    }
