import re
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
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow='\?id=[0-9]+$'),
            'parse_article',
            follow=True,
        ),
        Rule(SgmlLinkExtractor(allow='\?id=[0-9]+&com=1(&s=[0-9]+&no=[0-9]+){0,1}$'),
            'parse_comments',
            follow=True,
        ),
    )

    def _add_crawl_info(self, loader, response):
        loader.add_value('crawl_id', 1) # TODO: add crawl id.
        loader.add_value('crawl_timestamp', datetime.datetime.now())
        loader.add_value('crawl_url', response.url)
        loader.add_value('source_id', 'delfi.lt')

    def parse_comment(self, response, selector):
        loader = CommentLoader(item=CommentItem(), selector=selector)
        self._add_crawl_info(loader, response)

        loader.add_xpath('item_id', '@id')
        loader.add_value('item_link', "%s#%s" % (response.url,
                                                 loader.get_value('item_id')))

        loader.add_xpath('date', 'div[@class="comm-name"]/'
                                 'div[@class="font-small-gray"]/'
                                 'text()')
        loader.add_xpath('author', 'div[@class="comm-name"]/'
                                   'strong/text()')
        loader.add_xpath('content', 'div[@class="comm-text"]/div[1]/text()')

        loader.add_value('subject_type', models.SUBJECT_TYPE_ARTICLE)

        article_id = re.search('id=([0-9]+)', response.url).group(1)
        loader.add_value('subject_id', article_id)

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
