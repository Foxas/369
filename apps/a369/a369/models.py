# -*- coding: utf-8 -*-
from django.db import models

from djangosphinx import SphinxSearch
SUBJECT_TYPE_ARTICLE = 'article'


SUBJECT_CHOICES = (
    (SUBJECT_TYPE_ARTICLE, 'Article'),
)


class BaseItem(models.Model):
    crawl_timestamp = models.DateTimeField()
    crawl_id = models.CharField(max_length=255, blank=True)
    item_link = models.CharField(max_length=500, blank=True)
    source_id = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True


class ArticleItem(BaseItem):
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()


class CommentItem(BaseItem):
    """
    Main class
    """
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    subject_type = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    subject_id = models.CharField(max_length=255)

    search = SphinxSearch(index='main')

    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)

    class Admin:
        pass
