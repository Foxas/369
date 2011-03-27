import re
import datetime

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.link import Link

from crawler369.items import CommentItem, CommentLoader
from a369 import models


def _id_from_url(url):
    return re.search('id=([0-9]+)', url).group(1)


_crawled = []


class CommentsLinkExtractor():
    def __init__(self, source_id):
        self.source_id = source_id

    def _get_our_count(self, subject_id):
        query = {
            'subject_id': subject_id,
            'source_id': self.source_id,
        }
        objects = models.CommentItem.objects.filter(**query)
        count = objects.distinct('item_id').count()
        print count, query
        return count

    def extract_links(self, response):
        selector = HtmlXPathSelector(response)
        links_selector = selector.select('//a[@class="commentCount"]')
        links = []
        for a in links_selector:
            url = a.select('@href').extract()[0]
            subject_id = _id_from_url(url),
            count = a.select('text()').extract()[0]
            try:
                count = int(count.strip('()'))
            except:
                continue
            if subject_id in _crawled:
                continue
            _crawled.append(subject_id)
            our_count = self._get_our_count(subject_id)
            if count > our_count:
                links.append(url)
        return [Link(url=url) for url in links]


class CommentsPagesLinkExtractor():
    def __init__(self, source_id):
        self.source_id = source_id

    def extract_links(self, response):
        if not re.search('com=1', response.url):
            return []
        selector = HtmlXPathSelector(response)
        comment_links = selector.select('a[@class="ComNav"]')
        links = []
        for a in comment_links:
            url = a.select('@href').extract()[0]
            links.append(url)
        return [Link(url=url) for url in links]


class DelfiLt(CrawlSpider):
    source_id = 'delfi.lt'
    name = "delfi_lt"
    allowed_domains = ["delfi.lt"]
    start_urls = [
        "http://www.delfi.lt",
    ]

    rules = (
        Rule(CommentsLinkExtractor('delfi.lt'),
            'parse_comments',
            follow=True,
        ),
        Rule(CommentsPagesLinkExtractor('delfi.lt'),
            'parse_comments',
            follow=True,
        ),
    )

    def _add_crawl_info(self, loader, response):
        loader.add_value('crawl_id', 1) # TODO: add crawl id.
        loader.add_value('crawl_timestamp', datetime.datetime.now())
        loader.add_value('crawl_url', response.url)
        loader.add_value('source_id', self.source_id)

    def parse_comment(self, response, selector, extra_values, extra_xpath):
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


        for key, value in extra_xpath.items():
            loader.add_xpath(key, value)

        for key, value in extra_values.items():
            loader.add_value(key, value)

        item = loader.load_item()

        #try:
        #    item.save(commit=False)
        #except:
        #    import ipdb; ipdb.set_trace()

        return item

    def parse_comments(self, response):
        main_selector = HtmlXPathSelector(response)

        comments_xpath = '//div[@class="comm-container"]'
        subject_title_xpath = '//div[@class="title-medium"]/a/text()'

        comments_selector = main_selector.select(comments_xpath)
        subject_title_selector = main_selector.select(subject_title_xpath)

        extra_values = {
            'subject_type': models.SUBJECT_TYPE_ARTICLE ,
            'subject_id': _id_from_url(response.url),
        }

        extra_xpath = {
            'subject_title': subject_title_selector,
        }

        for selector in comments_selector:
            if not selector.select('@id'):
                continue
            yield self.parse_comment(response, selector, extra_values,
                                     extra_xpath)
