from django.core.paginator import Paginator
from django.template.loader import get_template

from annoying.decorators import render_to, ajax_request

from web369.models import ScrappedDocument


@render_to('index.html')
def index(request):
    return {}


@render_to('search_results.html')
def search_results(request):
    query = request.GET.get('q')
    if not query:
        return {'TEMPLATE': 'search_no_results.html'}
    results = ScrappedDocument.objects.search(query)
    pages = Paginator(results, 10)
    return {
        'results': results,
        'pages': pages,
        'page': pages.page(request.GET.get('page', 1)),
        'query': query,
    }
