# Scrapy settings for delfi_lt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawler369'
BOT_VERSION = '1.0'

SELECTORS_BACKEND = 'lxml'
SPIDER_MODULES = ['crawler369.spiders']
NEWSPIDER_MODULE = 'crawler369.spiders'
DEFAULT_ITEM_CLASS = 'crawler369.items.DelfiLtItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

