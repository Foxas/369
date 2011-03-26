from scrapy.contrib_exp.djangoitem import DjangoItem
from a369.models import OpinionItem


class CrawlerItem(DjangoItem):
    django_model = OpinionItem
