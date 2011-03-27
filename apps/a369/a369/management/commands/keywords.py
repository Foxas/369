import re
import operator
from optparse import make_option

from django.core.management.base import BaseCommand

from a369.models import CommentItem

RE_WORDS = re.compile(r'\w+')


class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    option_list = BaseCommand.option_list + (
        make_option('--limit',
            action='store',
            dest='limit',
            default=10,
            help='Limit to'),
        )


    def handle(self, *args, **options):
        all_words = {}
        for content in CommentItem.objects.values_list('content', flat=True):
            words = RE_WORDS.findall(content)
            for word in words:
                word = word.lower()
                if word in all_words:
                    all_words[word] += 1
                else:
                    all_words[word] = 1
        limit = int(options['limit'])
        if limit == 0:
            limit = -1
        for word, hits in sorted(all_words.iteritems(), key=operator.itemgetter(1), reverse=True):
            print hits, word
            limit -= 1
            if limit == 0:
                break
