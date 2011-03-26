# -*- coding: utf8 -*-
from scrapy.contrib.spiders import CrawlSpider
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request


count = 0

##The very basic spider, works
#class DelfiLtSpiderBasic(CrawlSpider):
    
    #name = "Delfi_lt_Basic"
    #allowed_dommains = ["delfi.lt"]
    ##start_urls = ["http://www.delfi.lt"]
    
    ##def parse(self, response):
        ##hxs =HtmlXPathSelector(response)
        ##comment_count_links = hxs.select("//a[@class='commentCount']")
        ##from scrapy.shell import inspect_response
        ###inspect_response(response)

class DelfiLtSpider(CrawlSpider):
    name = "Delfi_lt_default"
    allowed_dommains = ["delfi.lt"]
    #either start_urls should be defined, or the start_request method,
    #which returns iterable with the start_urls list
    #start_urls = ["http://www.delfi.lt"]
    
    def start_requests(self):
        """Request parameters
        (self, url, callback=None, method='GET', headers=None, body=None, 
                 cookies=None, meta=None, encoding='utf-8', priority=0.0,
                 dont_filter=False, errback=None):"""
        return [Request(url="http://www.delfi.lt",
                        callback=self.parse_homepage),]
    
    def parse_homepage(self, response):
        #import rpdb2
        #rpdb2.start_embedded_debugger("labas")
        import wingdbstub
        self.log("nu i ka")
        a=1
        response.body
        ref = response.url
        req = Request("http://www.alfa.lt",\
                      callback = lambda r: self.parse_each_link(r, ref),)
        #import rpdb2
        #rpdb2.start_embedded_debugger("labas")
        print "importing wingstub"
        a=1
        return req
        
    def parse_each_link(self,response, referer_url):
        self.log("Visited page %s from %s" % (response.url, referer_url))
    # scrapy.contrib.spiders.Rule(link_extractor, callback=None,\
    #cb_kwargs=None, follow=None, process_links=None, process_request=None)¶
    #link extractors have single purpose - extract links from a response object
    #Callback - callable or string to define which method to be used for parsing
    #the extracted link
    
    
    #rules = (
        ###Rule1
        #Rule(SgmlLinkExtractor(allow=(),deny=(), tags=('a'), attrs=('href', 'class')),\
             #),
             #)
    
    #def parse(self, response):
        #self.log("I'm in parse method")
        #hxs =HtmlXPathSelector(response)
        #comment_count_links = hxs.select("//a[@class='commentCount']")
    
    #def parse_commentcountlinks(self, response):
        #self.log("en")
        
    
        

#class DelfiLtSpider(CrawlSpider):
    
    #name = "Delfi_lt"
    #allowed_domains = ["delfi.lt"]
    #start_urls = ["http://www.delfi.lt"]
    
    #rules = (
        #Rule(SgmlLinkExtractor(allow='www.delfi.lt/.*id=\d+$'),\
                             ##   restrict_xpaths="//a[@class='commentCount']",),
            #'parse_comment_links',
            ##follow=True,
        #),
        #)
    
    
    ##rules = (
        ###1st rule        
        ##Rule(SgmlLinkExtractor(),
            ###restrict_xpaths="//a[@class=\"commentCount\"]",),\
            ##callback="parse_comment_links",
            ##follow=True,
            ##),
        
        ###2nd rule
        ##)
        
    
    #def parse_comment_links(self, response):
        #self.log("entered parse_comment_links")
        #global count
        #count += 1
        #print count
    
    ##def parse(self, response):
        ##self.log("entered parse")
        ##print "entered parse
        
#class BaseDelfiLt(BaseSpider):
    #name = "Delfi_lt_base"
    #allowed_domains = ["delfi.lt"]
    #start_urls = ["http://www.delfi.lt"]
    
    
    #def parse(self, response):
        #self.log('A response from %s just arrived!' % response.url)
        #hxs = HtmlXPathSelector(response)
        
        #for url in hxs.select("//a").extract():
            #yield Request(url, callback=self.parse)
        
    
    
    