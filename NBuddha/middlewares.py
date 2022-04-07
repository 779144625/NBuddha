# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class NbuddhaSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NbuddhaDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        request.cookies = {
            'SUB': '_2AkMWgb8Mf8NxqwJRmP4RzG7naIx2yQHEieKg3U7XJRMxHRl-yT9jqmATtRB6PQGR43h-HqDNZ1bNMxp4a0JmNeEt0DeZ',
            'SUBP': '0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWLlaH3bj3JGwREDS9inW4O',
            'XSRF-TOKEN': 'zbbiFby7OAC1KupkuIPDiQXh',
            '_s_tentry': 'weibo.com',
            'Apache': '6672890363463.748.1641885811025',
            'SINAGLOBAL': '6672890363463.748.1641885811025',
            'ULV': '1641885811034:1:1:1:6672890363463.748.1641885811025:',
            'WBPSESS': 'kErNolfXeoisUDB3d9TFH0i9qPkTt-RZ6mD_Do3tBzf4-duTaYQADWsPU8M-ud4BiocMQVXJ1ZuRMGHj9cCW3iUsZJjA6X3yocLQicGXYPyfBE3T9IUpPXrn5fURsDzxRgLXgqlaBXeUkMVNeTAdg6y3n_ukw_-kO8ft51CQUlg='
        }

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
