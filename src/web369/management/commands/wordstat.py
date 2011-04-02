# -*- encoding: utf-8 -*-

import re
import operator
import sys
from optparse import make_option

from django.core.management.base import BaseCommand

from web369.models import BaseWord, Word, ScrappedDocument


class Command(BaseCommand):
    args = ''
    help = 'Display statistic, highest ranked keywords, recount words'

    option_list = BaseCommand.option_list + (

        make_option('--limit', '-n',
            action='store',
            dest='limit',
            default=10,
            help='Number of most popular words to show'),

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
        print "\nStats:\n"
        print "  Base-words: %d" % BaseWord.objects.count()
        print "  Words: %d" % Word.objects.count()
        print "  Documents: %d" % ScrappedDocument.objects.count()
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
