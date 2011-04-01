# -*- coding: utf-8 -*-
import re
from django.db import models
from django.template.defaultfilters import wordcount
from django.dispatch import receiver

from web369.utils.strings import unicode_to_ascii, word_frequency, words


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


class BaseWordsManager(models.Manager):
    def merge(self, queryset):
        merge_to = queryset[0]
        for word in queryset[1:]:
            word.derivatives.update(base=merge_to)
            merge_to.count += word.count
            word.delete()
        merge_to.save()


class BaseWord(models.Model):
    word = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    stop_word = models.BooleanField(default=False)

    objects = BaseWordsManager()

    def __repr__(self):
        return "Word: %s Count: %s" % (self.word, self.count)

    def __str__(self):
        return self.word.encode('ascii', 'replace')

    def __unicode__(self):
        return self.word

    def derivatives_display(self):
        return ", ".join([unicode(w) for w in self.derivatives.all()])
    derivatives_display.short_description = "Derivatives"


class WordsManager(models.Manager):
    _cache = {}

    def get(self, word):
        return super(WordsManager, self).get(word=word)

    def get_or_create(self, word_str):
        word =  self._cache.get(word_str, None)
        if word:
            return word
        try:
            word = self.get_query_set().get(word=word_str)
        except Word.DoesNotExist:
            base = BaseWord(word=word_str)
            base.save()
            word = Word(word=word_str, base=base)
            word.save()
        return word


class Word(models.Model):
    word = models.CharField(max_length=255, primary_key=True, db_index=True)
    base = models.ForeignKey(BaseWord, related_name="derivatives")

    objects = WordsManager()

    def __str__(self):
        return self.word

    def __unicode__(self):
        return self.word

    def increase_count(self, count):
        assert self.base, \
            "You cannot increase count on word (%s) which is not saved" % self
        BaseWord.objects.filter(pk=self.base.pk) \
                        .update(count=models.F('count')+count)

    def cognate_words(self):
        return Word.objects.filter(base=self.base)


class ScrappedDocumentManager(models.Manager):
    def exists(self, item):
        if self.filter(source_id=item['source_id'],
                       subject_id=item['subject_id'],
                       item_id=item['item_id']).count():
            return True
        else:
            return False

    def build_search_query(self, querystring):
        querystring = unicode_to_ascii(querystring).lower()
        query = []
        for word in words(querystring):
            try:
                word = Word.objects.get(word)
                cognate_words = [w.word for w in word.cognate_words()]
                query.append('(%s)' % ' '.join(cognate_words))
            except Word.DoesNotExist:
                query.append(word)
        return ' +'.join(group for group in query)

    def search(self, querystring):
        querystring = self.build_search_query(querystring)
        where = 'MATCH(content_ascii, subject_title_ascii) AGAINST ("%s")'
        qs = self.all().extra(where=[where], params=[querystring])
        qs.search_query = querystring
        return qs


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


@receiver(models.signals.post_save, sender=ScrappedDocument)
def update_word_stats(sender, instance, created, using, **kwargs):
    if not created:
        return
    text = ''.join((instance.content_ascii, instance.subject_title_ascii))
    text = unicode_to_ascii(text).lower()
    for word, count in word_frequency(text, match="[a-z]{3,50}"):
        Word.objects.get_or_create(word).increase_count(count)
