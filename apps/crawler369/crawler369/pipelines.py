from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exceptions import DropItem
from a369 import models
from crawler369.items import CommentItem


class CommentsPipeline(object):
    def __init__(self):
        self.duplicates = {}
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_opened(self, spider):
        objects = models.CommentItem.objects.all()
        self.duplicates = set(objects.values_list('crawl_id', flat=True))

    def spider_closed(self, spider):
        del self.duplicates

    def process_item(self, item, spider):
        if not isinstance(item, CommentItem):
            return item
        try:
            if item['item_id'] in self.duplicates:
                raise DropItem("Duplicate item found: %s" % item)
        except KeyError:
            import ipdb; ipdb.set_trace()
        self.duplicates.add(item['item_id'])
        item.save()
        return item
