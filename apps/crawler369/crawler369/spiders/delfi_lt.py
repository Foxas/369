from scrapy.spider import BaseSpider


class DelfiLtComments(BaseSpider):
    name = "delfi_lt_comments"
    allowed_domains = ["delfi.lt"]
    start_urls = [
        "http://www.delfi.lt",
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)
