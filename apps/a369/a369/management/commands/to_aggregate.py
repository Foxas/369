# -*- coding: utf-8 -*-
import sys, re, fileinput, os, subprocess, commands, datetime
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option
from tsd.core.models import RssComment, Source
import feedparser, datetime

class Command(BaseCommand):
    """
    A class Command in a custom-command's module is a must.
    """
    help = "Prints hello world"
    args = '[various KEY=val options, use `runfcgi help` for help]'  
    
    def handle(self, *args, **options):
        """
        A must-be-inplemented method, which is launched fist.
        """
        option_list = BaseCommand.option_list + (
        make_option("-o", "--source_meta", dest="source_metadata",\
                    default=1),
        )
        sqs = Source.objects.all()
        for source in sqs:
            rss = feedparser.parse(source.feed_url)
            print rss.feed.title
            for entry in rss['entries']:
                a = RssComment()
                a.url = entry['link']
                a.nickas = source.username
                a.source = source
                a.content = entry['title']
                a.date = convert_mtime_to_datetime(entry['updated_parsed'])
                a.full_clean()
                a.save()


def convert_mtime_to_datetime(mtime):
    dt = datetime.datetime(mtime.tm_year, mtime.tm_mon, mtime.tm_mday,\
                           mtime.tm_hour, mtime.tm_min, mtime.tm_sec)
    return dt