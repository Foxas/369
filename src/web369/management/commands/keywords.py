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
        )


    def handle(self, *args, **options):
        limit = int(options['limit'])
        words = BaseWord.objects.filter(stop_word=False)\
                                .order_by('-count')[:limit]
        for word in words:
            print "%s: %d" % (word, word.count)
