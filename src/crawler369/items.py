import datetime
from scrapy.contrib_exp.djangoitem import DjangoItem
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join
from web369 import models


class CommentItem(DjangoItem):
    django_model = models.ScrappedDocument



class CommentLoader(XPathItemLoader):
    def __init__(self, *args, **kwargs):
        super(CommentLoader, self).__init__(*args, **kwargs)
        self.add_value('document_type', models.DOCUMENT_TYPE.COMMENT)

    default_output_processor = TakeFirst()

    @MapCompose
    def date_in(value):
        return datetime.datetime.strptime(value, '%Y %m %d %H:%M')

    @MapCompose
    def item_id_in(value):
        return int(value.strip('c'))

    subject_id_in = MapCompose(int)
    source_id = MapCompose(int)

    content_out = Join()

    author_out = Join()
