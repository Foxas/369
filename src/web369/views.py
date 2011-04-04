from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page

from annoying.decorators import render_to

from web369.models import ScrappedDocument, BaseWord, SearchQuery


@cache_page(60 * 60)
@render_to('index.html')
def index(request):
    top_words = BaseWord.objects.filter(stop_word=False) \
                                .with_count() \
                                .order_by('-count')
    return {'recent_trends': top_words[:4],
            'month_trends': top_words[4:10],
            'alltime_trends': top_words[10:18]}


@render_to('search_results.html')
def search_results(request):
    query = SearchQuery(request.GET.get('q'))
    if not query:
        return {'TEMPLATE': 'search_no_results.html'}
    results = ScrappedDocument.objects.search(query)
    pages = Paginator(results, 10)
    return {
        'results': results,
        'pages': pages,
        'page': pages.page(request.GET.get('page', 1)),
        'query': results.search_query,
    }
