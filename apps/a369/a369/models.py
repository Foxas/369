# -*- coding: utf-8 -*-
import re
from django.db import models

from djangosphinx import SphinxSearch
from django.template.defaultfilters import wordcount

SUBJECT_TYPE_ARTICLE = 1

SUBJECT_CHOICES = (
    (SUBJECT_TYPE_ARTICLE, 'Article'),
)



class BaseItem(models.Model):
    crawl_timestamp = models.DateTimeField()
    crawl_id = models.CharField(max_length=255, blank=True)
    crawl_url = models.CharField(max_length=255, blank=True)
    source_id = models.CharField(max_length=255, blank=True) # example delfi.lt
    item_id = models.CharField(max_length=255, blank=True)
    item_link = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True


class ArticleItem(BaseItem):
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()


class CommentBase(models.Model):
    subject_type = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    subject_id = models.CharField(max_length=255)


class CommentItem(BaseItem):
    """
    Main class
    """
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    content_length = models.IntegerField(default=0, null=True)
    content_word_count = models.IntegerField(default=0, null=True)
    subject_type = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    subject_id = models.CharField(max_length=255)

    search = SphinxSearch(index='main')

    subject_title = 'Subject title'

    def __unicode__(self):
        return u'%s (#%s), %s by %s' % (self.id, self.crawl_id, self.date, 
                                        self.author)

    class Admin:
        pass

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        content = re.sub('[!-@[-`]', ' ', self.content)
        content = re.sub(' +', ' ', self.content)
        self.content_word_count = wordcount(content)


class TweetItem(BaseItem):
    """
    Main class
    """
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    content_length = models.IntegerField(default=0, null=True)
    content_word_count = models.IntegerField(default=0, null=True)
    subject_type = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    subject_id = models.CharField(max_length=255)

    search = SphinxSearch(index='main')

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        content = re.sub('[!-@[-`]', ' ', self.content)
        content = re.sub(' +', ' ', self.content)
        self.content_word_count = wordcount(content)
