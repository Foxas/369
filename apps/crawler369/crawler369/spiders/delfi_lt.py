import datetime

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.loader import XPathItemLoader

from crawler369.items import CommentItem
from a369 import models

class DelfiLt(CrawlSpider):
    name = "delfi_lt"
    allowed_domains = ["delfi.lt"]
    start_urls = [
        "http://www.delfi.lt",
        "http://www.delfi.lt/news/ringas/lit/rcekutis-atsakymas-dkuoliui-apie-zudoma-valstybe.d?id=43602903&com=1",
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow='\?id=[0-9]+$'),
            'parse_article',
            follow=True,
        ),
        Rule(SgmlLinkExtractor(allow='\?id=[0-9]+&com=1'),
            'parse_comments',
            follow=True,
        ),
    )

    def parse_comments(self, response):
        main_selector = HtmlXPathSelector(response)
        import ipdb; ipdb.set_trace()

        comments_xpath = '//div[@class="comm-container"]'
        comments_selector = main_selector.select(comments_xpath)

        for selector in comments_selector:
            item = CommentItem()
            loader = XPathItemLoader(item=item, selector=selector)
            loader.add_xpath('crawl_id', '@id')
            loader.add_xpath('date', )
            loader.add_xpath('author', )
            loader.add_xpath('content', )

            item.crawl_timestamp = datetime.datetime.now()
            item.subject_type = models.SUBJECT_TYPE_ARTICLE
            item.subject_id = 'todo'

    def parse_article(self, response):
        pass
