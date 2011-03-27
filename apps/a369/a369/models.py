# -*- coding: utf-8 -*-
import re
from django.db import models

from djangosphinx import SphinxSearch
from django.template.defaultfilters import wordcount

class SOURCE_ID:
    DELFI_LT = 1

SUBJECT_TYPE_ARTICLE = 1

SUBJECT_CHOICES = (
    (SUBJECT_TYPE_ARTICLE, 'Article'),
)



class BaseItem(models.Model):
    crawl_timestamp = models.DateTimeField()
    crawl_id = models.CharField(max_length=255, blank=True)
    crawl_url = models.CharField(max_length=255, blank=True)
    source_id = models.IntegerField()
    item_id = models.IntegerField()
    item_link = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True


class ArticleItem(BaseItem):
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()


class CommentItemsManager(models.Manager):
    def exists(self, item):
        if self.filter(source_id=item['source_id'],
                       subject_id=item['subject_id'],
                       item_id=item['item_id']).count():
            return True
        else:
            return False


class CommentItem(BaseItem):
    """
    Main class
    """
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    content_length = models.IntegerField(default=0, null=True)
    content_word_count = models.IntegerField(default=0, null=True)
    subject_title = models.CharField(max_length=555, null=True)
    subject_type = models.CharField(max_length=255, choices=SUBJECT_CHOICES)
    subject_id = models.IntegerField(unique=True)

    unique_together = (("source_id", "subject_id", "item_id"),)

    search = SphinxSearch(index='main')

    objects = CommentItemsManager()

    def __unicode__(self):
        return u'%s (#%s), %s by %s' % (self.id, self.crawl_id, self.date, 
                                        self.author)

    def get_iq_score(self):
        ratio = self.content_length / self.content_word_count
        return (ratio+5)**2

    class Admin:
        pass

    def get_absolute_url(self):
        return str(self.item_link).replace('item_id', 'c%s' % self.item_id)

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        content = re.sub('[!-@[-`]', ' ', self.content)
        content = re.sub(' +', ' ', self.content)
        self.content_word_count = wordcount(content)
        super(CommentItem, self).save(*args, **kwargs)

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
