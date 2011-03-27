import re
import datetime

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.link import Link

from crawler369.items import CommentItem, CommentLoader
from a369 import models


def _id_from_url(url):
    if isinstance(url, Link):
        url = url.url
    return int(re.search('id=([0-9]+)', url).group(1))


_crawled = []


class HtmlCommentsCount(object):
    def __init__(self, selector, xpath=None):
        if xpath:
            selector = selector.select(xpath)
        self.selector = selector

    def get_count(self):
        try:
            return int(self.select('text()').extract()[0].strip('()'))
        except:
            return 0

    def get_url(self):
        return Link(self.select('@href').extract()[0])

    def get_subject_id(self):
        return _id_from_url(self.get_url())

    def __getattr__(self, attr):
        return getattr(self.selector, attr)


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
        return count

    def extract_links(self, response):
        if not 'http://www.delfi.lt' == str(response.url).strip('/'):
            return []
        selector = HtmlXPathSelector(response)
        links_selector = selector.select('//div[@class="delfi-content"][1]//a[@class="commentCount"]')
        links = []
        for a in links_selector:
            comments_count = HtmlCommentsCount(a)
            subject_id = comments_count.get_subject_id()
            if subject_id in _crawled:
                continue
            _crawled.append(subject_id)
            if comments_count.get_count() > self._get_our_count(subject_id):
                links.append(comments_count.get_url())
                print "Added: %s" % subject_id
            else:
                print "Skiped: %s" % subject_id
        return links


class CommentPaginationLinkExtractor():
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
    source_id = models.SOURCE_ID.DELFI_LT
    name = "delfi_lt"
    allowed_domains = ["delfi.lt"]
    start_urls = [
        "http://www.delfi.lt",
    ]

    rules = (
        Rule(CommentsLinkExtractor(models.SOURCE_ID.DELFI_LT),
            'parse_comments',
            follow=True,
        ),
        Rule(CommentPaginationLinkExtractor(models.SOURCE_ID.DELFI_LT),
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

        loader.add_value('item_link',
                         "%s#%s" % (response.url,
                                    selector.select('@id').extract()[0]))

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

        return loader.load_item()

    def parse_comments(self, response):
        main_selector = HtmlXPathSelector(response)

        comments_xpath = '//div[@class="comm-container"]'
        subject_title_xpath = '//div[@class="title-medium"]/a/text()'

        comments_selector = main_selector.select(comments_xpath)

        extra_values = {
            'subject_type': models.SUBJECT_TYPE_ARTICLE ,
            'subject_id': _id_from_url(response.url),
        }

        extra_xpath = {
            'subject_title': subject_title_xpath,
        }

        for selector in comments_selector:
            if not selector.select('@id'):
                continue
            yield self.parse_comment(response, selector, extra_values,
                                     extra_xpath)


class DelfiLtQuick(DelfiLt):
    name = "delfi_lt_quick"
    start_urls = [
        'http://www.delfi.lt/news/daily/world/radiacija-fukusimos-ae-antrajame-reaktoriuje-10-mln-kartu-virsija-norma.d?id=43629471',
        'http://www.delfi.lt/news/daily/lithuania/mkvedaravicius-cecenijoje-dauguma-vyru-miega-apsirenge.d?id=43669815',
        'http://verslas.delfi.lt/law/komentara-apie-gejus-parases-ukininkas-gavo-bauda-ir-neteko-kompiuterio.d?id=43673113',
        'http://gyvenimas.delfi.lt/vestuves/santuoka-rugpjuti-reikia-uzsisakyti-pries-metus-pusantru.d?id=43669581',
        'http://www.delfi.lt/news/daily/world/zemes-valandai-keliaujant-aplink-planeta-sviesos-uzgesdavo-ir-ispudinguose-pastatuose-ir-paprastuose-namuose.d?id=43671123',
    ]

    rules = (
        Rule(CommentPaginationLinkExtractor(models.SOURCE_ID.DELFI_LT),
            'parse_comments',
            follow=True,
        ),
    )
