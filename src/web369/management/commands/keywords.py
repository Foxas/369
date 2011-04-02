# -*- encoding: utf-8 -*-

import re
import operator
import sys
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
            default=10,
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
        limit = int(options['limit']) or 10
        words = BaseWord.objects.filter(stop_word=False) \
                                .with_count() \
                                .order_by('-count')[:limit]
        print "\nMost popular words:\n"
        for word in words:
            print u"%5d | %s" % (word.count, word)

    def recount(self):
        perc = False
        print "\nCounting words...\n"
        for msg in BaseWord.objects.recount_proc():
            if re.match('[0-9]+%', msg):
                if perc:
                    sys.stdout.write('\b' * perc)
                sys.stdout.write(msg)
                sys.stdout.flush()
                perc = len(msg)
            else:
                if perc:
                    print "\n",
                perc = False
                print "  ", msg, '',
                sys.stdout.flush()
        print "\n"
        print "words recount done."
