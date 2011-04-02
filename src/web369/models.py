# -*- coding: utf-8 -*-
import re
import sys
from django.db import models
from django.template.defaultfilters import wordcount
from django.dispatch import receiver
from django.conf import settings

from web369.utils.strings import unicode_to_ascii, count_words, split_words


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


class BaseWordQuerySet(models.query.QuerySet):
    def with_count(self):
        return self.annotate(count=models.Sum('derivatives__count'))


class BaseWordManager(models.Manager):
    def with_count(self):
        return self.get_query_set().with_count()

    def merge(self, queryset):
        merge_to = queryset[0]
        for word in queryset[1:]:
            word.derivatives.update(base=merge_to)
            merge_to.count += word.count
            word.delete()
        merge_to.save()

    def recount(self, verbose=False):
        word_stats = ScrappedDocument.objects.word_stats(verbose=verbose)
        if verbose:
            total = len(word_stats)
            counter = 0
            step_counter = 0
            step = total / 100.0
            print "Saving statistic of %d words to database..." % total
            print "0%"
        for word, count in word_stats.items():
            Word.objects.set_count(word, count)
            if verbose:
                if counter > step_counter * step:
                    step_counter = step_counter + 1
                    print "%d%%" % step_counter
                counter = counter + 1

    def get_query_set(self):
        return BaseWordQuerySet(model=self.model)


class BaseWord(models.Model):
    word = models.CharField(max_length=255)
    stop_word = models.BooleanField(default=False)
    count = None

    objects = BaseWordManager()

    def __repr__(self):
        if hasattr(self, 'count'):
            return "BaseWord: %s (%d)"  % (self.word, self.count)
        else:
            return "BaseWord: %s" % self.word

    def __str__(self):
        return self.word.encode('ascii', 'replace')

    def __unicode__(self):
        return self.word

    def derivatives_display(self):
        return ", ".join([unicode(w) for w in self.derivatives.all()])
    derivatives_display.short_description = "Derivatives"

    def count_display(self):
        return self.count
    count_display.short_description = "Word count"
    count_display.admin_order_field = 'count'


class WordManager(models.Manager):
    def get(self, word):
        return super(WordManager, self).get(word=word)

    def create(self, word, count=0, commit=True):
        base = BaseWord(word=word)
        base.save()
        word_obj = Word(word=word, base=base, count=0)
        if commit:
            word_obj.save()
        return word_obj

    def get_or_create(self, word, commit=True):
        """ Returns tuple: (word, created). ``created`` is true if word has been
        created """
        try:
            return self.get(word), False
        except Word.DoesNotExist:
            return self.create(word, 0, commit), True

    def set_count(self, word, count):
        count = Word.objects.filter(word=word) \
                            .update(count=count)
        if not count:
            self.create(word, count)

    def increase_count(self, word, count):
        count = Word.objects.filter(word=word) \
                            .update(count=models.F('count')+count)
        if not count:
            self.create(word, count)


class Word(models.Model):
    word = models.CharField(max_length=255, primary_key=True, db_index=True)
    base = models.ForeignKey(BaseWord, related_name="derivatives")
    count = models.IntegerField(default=0)

    objects = WordManager()

    def __str__(self):
        return self.word

    def __unicode__(self):
        return self.word

    def cognate_words(self):
        return Word.objects.filter(base=self.base)


class ScrappedDocumentQuerySet(models.query.QuerySet):
    def word_stats(self, verbose=False):
        word_stats = {}
        if verbose:
            counter = 0
            total = self.count()
            step = total / 100.0
            step_counter = 0
            print "Collecting word statistic of %d objects..." % total
            print "0%"
        for document in self:
            for word, count in document.word_stats():
                word_stats[word] = word_stats.get(word, 0) + count
            if verbose:
                if counter > step_counter * step:
                    step_counter = step_counter + 1
                    print "%d%%" % step_counter
                counter = counter+1
        return word_stats


class ScrappedDocumentManager(models.Manager):
    def word_stats(self, verbose=False):
        return self.get_query_set().word_stats(verbose=verbose)

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
        for word in split_words(querystring):
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

    def get_query_set(self):
        return ScrappedDocumentQuerySet(model=self.model)


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

    def word_stats(self):
        text = ' '.join([self.subject_title_ascii or "",
                         self.content_ascii or ""]).lower()
        if "none" in split_words(text):
            import ipdb; ipdb.set_trace()
        return count_words(text)

    def get_absolute_url(self):
        return str(self.item_link).replace('item_id', 'c%s' % self.item_id)

    def save(self, *args, **kwargs):
        self.content_length = len(self.content)
        content = re.sub('[!-@[-`]', ' ', self.content)
        content = re.sub(' +', ' ', self.content)
        self.content_word_count = wordcount(content)
        self.content_ascii = unicode_to_ascii(self.content)
        self.subject_title_ascii = unicode_to_ascii(self.subject_title)
        super(ScrappedDocument, self).save(*args, **kwargs)


if settings.LIVE_WORD_COUNT:
    @receiver(models.signals.post_save, sender=ScrappedDocument)
    def update_word_stats(sender, instance, created, using, **kwargs):
        if not created:
            return
        text = ''.join((instance.content_ascii, instance.subject_title_ascii))
        text = unicode_to_ascii(text).lower()
        for word, count in count_words(text):
            Word.objects.increase_count(word, count)
