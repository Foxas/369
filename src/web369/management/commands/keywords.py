# -*- encoding: utf-8 -*-

import re
import operator
from optparse import make_option

from django.core.management.base import BaseCommand

from web369.models import BaseWord


class Command(BaseCommand):
    args = ''
    help = 'Display highest ranked keywords'

    option_list = BaseCommand.option_list + (

        make_option('--limit',
            action='store',
            dest='limit',
            default=50,
            help='Limit to'),

        make_option('--recount',
            action='store_true',
            dest='recount',
            default=False,
            help='Recount all keywords.'),
    )

    def handle(self, *args, **options):
        if options['recount']:
            self.recount()
        limit = int(options['limit']) or 50
        words = BaseWord.objects.filter(stop_word=False) \
                                .with_count() \
                                .order_by('-count')[:limit]
        for word in words:
            print u"%9d | %s" % (word.count, word)

    def recount(self):
        BaseWord.objects.recount(verbose=True)
