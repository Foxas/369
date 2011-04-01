# -*- coding: utf-8 -*-
import re
from django.db import models
from django.template.defaultfilters import wordcount

from web369.utils.strings import unicode_to_ascii


class DOCUMENT_TYPE:
    COMMENT = 1


class SOURCE_ID:
    DELFI_LT = 1


class SUBJECT_TYPE:
    ARTICLE = 1


def _choices(obj):
    choices = []
    for attr in dir(obj):
        if attr.startswith('__'):
            continue
        choices.append(
            (getattr(obj, attr), attr.title())
        )
    return choices


class ScrappedDocumentManager(models.Manager):
    def exists(self, item):
        if self.filter(source_id=item['source_id'],
                       subject_id=item['subject_id'],
                       item_id=item['item_id']).count():
            return True
        else:
            return False

    def search(self, query):
        query = unicode_to_ascii(query)
        where = 'MATCH(content_ascii, subject_title_ascii) AGAINST ("%s")'
        return self.all().extra(where=[where], params=[query])


class ScrappedDocument(models.Model):
    """
    Scrapped document.
    """
    document_type = models.IntegerField(choices=_choices(DOCUMENT_TYPE))
    crawl_timestamp = models.DateTimeField()
    crawl_id = models.CharField(max_length=255, blank=True)
    crawl_url = models.CharField(max_length=255, blank=True)
    source_id = models.IntegerField(choices=_choices(SOURCE_ID))
    item_id = models.IntegerField()
    item_link = models.CharField(max_length=500, blank=True)
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    content_ascii = models.TextField() # for full text searches
    content_length = models.IntegerField(default=0, null=True)
    content_word_count = models.IntegerField(default=0, null=True)
    subject_title = models.CharField(max_length=555, null=True)
    subject_title_ascii = models.CharField(max_length=555, null=True)
    subject_type = models.CharField(max_length=255, 
                                    choices=_choices(SUBJECT_TYPE))
    subject_id = models.IntegerField()

    unique_together = (("source_id", "subject_id", "item_id"),)

    objects = ScrappedDocumentManager()

    def __unicode__(self):
        return u'%s (#%s), %s by %s' % (self.id, self.crawl_id, self.date, 
                                        self.author)

    def get_iq_score(self):
        ratio = self.content_length / self.content_word_count
        return (ratio+5)**2

    def get_absolute_url(self):
        return str(self.item_link).replace('item_id', 'c%s' % self.item_id)

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        content = re.sub('[!-@[-`]', ' ', self.content)
        content = re.sub(' +', ' ', self.content)
        self.content_word_count = wordcount(content)
        self.content_ascii = unicode_to_ascii(self.content)
        self.subject_title_ascii = unicode_to_ascii(self.subject_title_ascii)
        super(ScrappedDocument, self).save(*args, **kwargs)
