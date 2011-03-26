import datetime

from djangosphinx.apis.current import SPHINX_API_VERSION

from annoying.decorators import render_to

from .models import CommentItem


@render_to('index.html')
def index(request):
    kintamasis = SPHINX_API_VERSION
    return {'variable': kintamasis}


@render_to('search_results.html')
def search_results(request):
    q = request.GET.get('q')
    results = {'results': CommentItem.search.query(q)}
    results = results['results']
    list(results)
    return results
