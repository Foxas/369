from twisted.application.service import Service, Application
from twisted.python import log as txlog

from scrapy import log
from scrapy.crawler import Crawler
from scrapy.conf import settings

class CrawlerService(Service):

    def startService(self):
        settings.overrides['QUEUE_CLASS'] = settings['SERVER_QUEUE_CLASS']
        self.crawler = Crawler(settings)
        self.crawler.install()
        self.crawler.start()

    def stopService(self):
        return self.crawler.stop()

def get_application(logfile, loglevel=log.DEBUG):
    app = Application("Scrapy")
    app.setComponent(txlog.ILogObserver, \
        log.ScrapyFileLogObserver(open(logfile, 'a'), loglevel).emit)
    CrawlerService().setServiceParent(app)
    return app

application = get_application('scrapy.log')
