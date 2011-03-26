from scrapy.contrib_exp.djangoitem import DjangoItem
from a369 import models


class ArticleItem(DjangoItem):
    django_model = models.ArticleItem


class CommentItem(DjangoItem):
    django_model = models.CommentItem

