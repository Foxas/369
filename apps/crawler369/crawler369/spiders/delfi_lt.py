import datetime

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from crawler369.items import CommentItem, CommentLoader
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

    def parse_comment(self, response, selector):
        loader = CommentLoader(item=CommentItem(), selector=selector)

        loader.add_xpath('crawl_id', '@id')
        loader.add_xpath('date', 'div[@class="comm-name"]/'
                                 'div[@class="font-small-gray"]/'
                                 'text()')
        loader.add_xpath('author', 'div[@class="comm-name"]/'
                                   'strong/text()')
        loader.add_xpath('content', 'div[@class="comm-text"]/div[1]/text()')

        loader.add_value('crawl_timestamp', datetime.datetime.now())
        loader.add_value('subject_type', models.SUBJECT_TYPE_ARTICLE)
        loader.add_value('subject_id', 'todo')
        loader.add_value('item_link', "%s#%s" % (response.url,
                                                  loader.get_value('crawl_id')))
        loader.add_value('source_id', 'delfi.lt')

        item = loader.load_item()

        return item

    def parse_comments(self, response):
        main_selector = HtmlXPathSelector(response)

        comments_xpath = '//div[@class="comm-container"]'
        comments_selector = main_selector.select(comments_xpath)

        for selector in comments_selector:
            yield self.parse_comment(response, selector)


    def parse_article(self, response):
        pass
