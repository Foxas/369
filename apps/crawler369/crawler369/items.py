# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib_exp.djangoitem import DjangoItem
from tsd.core.models import Documents

class DelfiLtItem(DjangoItem):
    # define the fields for your item here like:
    # name = Field()
    django_model = Documents

class Dmoz(Item):
    title = Field()
    link = Field()
    desc = Field()
    
    
    
