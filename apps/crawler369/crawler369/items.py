import datetime
from scrapy.contrib_exp.djangoitem import DjangoItem
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from a369 import models


class ArticleItem(DjangoItem):
    django_model = models.ArticleItem


class CommentItem(DjangoItem):
    django_model = models.CommentItem


class CommentLoader(XPathItemLoader):
    default_output_processor = TakeFirst()

    @MapCompose
    def date_in(value):
        return datetime.datetime.strptime(value, '%Y %m %d %H:%M')

    content_out = Join()

    author = Join()
