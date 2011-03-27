from scrapy.exceptions import DropItem
from a369 import models
from crawler369.items import CommentItem


class CommentsPipeline(object):
    def process_item(self, item, spider):
        if not isinstance(item, CommentItem):
            return item
        if models.CommentItem.objects.exists(item):
            raise DropItem("Duplicate item found: %s" % item)
        item.save()
        return item
