import datetime

from djangosphinx.apis.current import SPHINX_API_VERSION

from annoying.decorators import render_to


@render_to('index.html')
def index(request):
    kintamasis = SPHINX_API_VERSION
    return {'variable': kintamasis}


@render_to('search_results.html')
def search_results(request):
    return {}
