# -*- coding: utf-8 -*-
from django.db import models

class BaseItem(models.Model):
    crawl_timestamp = models.DateTimeField()
    crawl_id = models.CharField(max_length=255, blank=True)
    item_link = models.CharField(max_length=500, blank=True)
    source_id = models.CharField(max_length=500, blank=True)

    class Meta:
        abstract = True

class OpinionItem(BaseItem):
    """
    Main class
    """
    date = models.DateTimeField()
    author = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)

    class Admin:
        pass
