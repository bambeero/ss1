import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from contacts.items import ContactsItem

class AswaqcityComSpider(BaseSpider):
    name = 'aswaqcity.com'
    allowed_domains = ['aswaqcity.com']

    def start_requests(self):
        yield Request('http://www.aswaqcity.com', callback=self.parse_cities)

    def parse_cities(self, response):
        hxs = HtmlXPathSelector(response)

        for city in hxs.select(u'//td[@class="alt1Active"]//a'):
            url = urljoin_rfc(get_base_url(response), city.select(u'./@href').extract()[0])
            if url in (
                    'http://www.aswaqcity.com/forum782.html',
                    'http://www.aswaqcity.com/forum749.html',
                    'http://www.aswaqcity.com/forum750.html',
                    'http://www.aswaqcity.com/forum655.html',
                    ):
                continue
            yield Request(url, callback=self.parse_threads,
                    meta={'city': ' '.join(city.select(u'./text()').extract()[0].split()[2:-1])})

    def parse_threads(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//div[@class="pagenav"]//a/@href').extract():
            yield Request(url, callback=self.parse_threads, meta=response.meta)

        for url in hxs.select(u'//a[starts-with(@id, "thread_title_")]/@href').extract():
            yield Request(url, callback=self.parse_thread, meta=response.meta)

    def parse_thread(self, response):
        hxs = HtmlXPathSelector(response)

        for post in hxs.select(u'//div[@id="posts"]//table[starts-with(@id, "post")]'):
            post_html = ''.join(post.select(u'.//div[starts-with(@id, "post_message_")]/node()').extract()).strip()
            phone_number = re.search('(05\d{8})', post_html)
            if phone_number:
                item = ContactsItem()
                item['city'] = response.meta['city']
                item['phone_number'] = phone_number.groups()[0]
                yield item

        for url in hxs.select(u'//div[@class="pagenav"]//a/@href').extract():
            yield Request(url, callback=self.parse_thread, meta=response.meta)
