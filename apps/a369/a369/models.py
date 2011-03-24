# -*- coding: utf-8 -*-
from django.db import models
from djangosphinx.models import SphinxSearch
from datetime import datetime

class Documents(models.Model):
    """
    Main class
    """
    id = models.AutoField(primary_key=True)
    source_type = models.CharField(max_length=2295)
    source = models.CharField(max_length=2295)
    date_birth = models.DateTimeField() 
    #data kuomet komentaras buvo paliktas
    title = models.CharField(max_length=2295, blank=True)
    # defli atveju - straipsnio pavadinimas
    # newsgroup'u atveju, forumu - topic'as
    # blogu atveju - straipsnio pavadinimas
    # twitter ir IRC atveju - empty
    nickas = models.CharField(max_length=2295, blank=True)
    #defli - nickas
    #twitter - username'as arba loginas account'o
    linkas = models.CharField(max_length=2295, blank=True)
    content = models.TextField() #pats tekstas
    #unique_row = models.CharField(unique=True, max_length=150)
    ts_insert = models.DateTimeField(default=datetime.now)
    source_id = models.IntegerField()
    surrogate_key = models.CharField(max_length=39) #unique=True
    class Meta:
        db_table = u'documents'
    def __unicode__(self):
        return u'%s %s' % (self.id, self.title)
        #return u'%s %s %s' % (self.id, self.title, self.content)
    
    class Admin:
        pass

  
class Source(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=2295)
    username = models.CharField(max_length=2295, blank=True)
    screen_name = models.CharField(max_length=2295, blank=True)
    sourcee_id = models.IntegerField(blank=True)
    feed_url = models.CharField(max_length=2295, blank=True)
    homepage = models.CharField(max_length=2295, blank=True)
    
    def __unicode__(self):
        return u'%s %s' % (self.id, self.username)
    
    class Admin:
        pass

class RssComment(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.ForeignKey(Source)
    content = models.TextField()
    url = models.CharField(max_length=2295, blank=True)
    nickas = models.CharField(max_length=2295, blank=True)
    date = models.DateTimeField(blank=False)
    ts_insert=models.DateTimeField(auto_now_add=True)

    
    def __unicode__(self):
        return u'%s %s' % (self.id, self.nickas)
    
    class Admin:
        pass