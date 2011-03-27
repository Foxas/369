#!/usr/bin/python

import sys
try:
    if sys.argv[1] == '-u':
        sys.argv.remove('-u')
except:
    pass


sys.path[0:0] = [
    '/usr/lib/python2.6/dist-packages/PIL',
    '/home/toinbis/.buildout/eggs/South-0.7.3-py2.6.egg',
    '/home/toinbis/.buildout/eggs/django_annoying-0.7.6-py2.6.egg',
    '/home/toinbis/Desktop/programming/369.lt/apps/crawler369',
    '/home/toinbis/Desktop/programming/369.lt/apps/a369',
    '/home/toinbis/Desktop/programming/369.lt/parts/django-sphinx',
    '/home/toinbis/.buildout/eggs/pysolr-2.0.13-py2.6.egg',
    '/home/toinbis/.buildout/eggs/Scrapy-0.12.0.2539-py2.6.egg',
    '/home/toinbis/.buildout/eggs/Twisted-10.2.0-py2.6-linux-i686.egg',
    '/home/toinbis/.buildout/eggs/coverage-3.4-py2.6-linux-i686.egg',
    '/home/toinbis/.buildout/eggs/django_debug_toolbar-0.8.4-py2.6.egg',
    '/home/toinbis/.buildout/eggs/django_extensions-0.6-py2.6.egg',
    '/home/toinbis/.buildout/eggs/django_test_utils-0.3-py2.6.egg',
    '/home/toinbis/.buildout/eggs/ipdb-0.3-py2.6.egg',
    '/home/toinbis/.buildout/eggs/ipython-0.10.1-py2.6.egg',
    '/home/toinbis/.buildout/eggs/BeautifulSoup-3.2.0-py2.6.egg',
    '/home/toinbis/.buildout/eggs/zope.interface-3.6.1-py2.6-linux-i686.egg',
    '/usr/lib/python2.6/dist-packages',
    '/home/toinbis/Desktop/programming/369.lt/parts/django',
    '/home/toinbis/.buildout/eggs/distribute-0.6.15-py2.6.egg',
    ]

_interactive = True
if len(sys.argv) > 1:
    _options, _args = __import__("getopt").getopt(sys.argv[1:], 'ic:m:')
    _interactive = False
    for (_opt, _val) in _options:
        if _opt == '-i':
            _interactive = True
        elif _opt == '-c':
            exec _val
        elif _opt == '-m':
            sys.argv[1:] = _args
            _args = []
            __import__("runpy").run_module(
                 _val, {}, "__main__", alter_sys=True)

    if _args:
        sys.argv[:] = _args
        __file__ = _args[0]
        del _options, _args
        execfile(__file__)

if _interactive:
    del _interactive
    __import__("code").interact(banner="", local=globals())
