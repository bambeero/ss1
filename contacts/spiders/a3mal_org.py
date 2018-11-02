import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from contacts.items import ContactsItem

class A3malOrgtSpider(BaseSpider):
    name = 'a3mal.org'
    allowed_domains = ['a3mal.org']

    def start_requests(self):
        yield Request('http://www.a3mal.org', callback=self.parse_cities)

    def parse_cities(self, response):
        hxs = HtmlXPathSelector(response)

        for city in hxs.select(u'//td[@class="alt1Active"]//a'):
            url = urljoin_rfc(get_base_url(response), city.select(u'./@href').extract()[0])
            if url not in (
                'http://a3mal.org/f20.html',
                'http://a3mal.org/f21.html',
                'http://a3mal.org/f43.html',
                'http://a3mal.org/f42.html',
                'http://a3mal.org/f23.html',
                'http://a3mal.org/f24.html',
                'http://a3mal.org/f25.html',
                'http://a3mal.org/f26.html',
                'http://a3mal.org/f27.html',
                'http://a3mal.org/f29.html',
                'http://a3mal.org/f30.html',
                'http://a3mal.org/f31.html',
                'http://a3mal.org/f32.html',
                'http://a3mal.org/f33.html',
                'http://a3mal.org/f34.html',
                'http://a3mal.org/f35.html',
                'http://a3mal.org/f37.html',
                'http://a3mal.org/f38.html',
                'http://a3mal.org/f39.html',
                'http://a3mal.org/f40.html',
                'http://a3mal.org/f44.html',
                'http://a3mal.org/f45.html',
                'http://a3mal.org/f46.html',):
                continue
            yield Request(url, callback=self.parse_threads,
                    meta={'city': ' '.join(city.select(u'./strong/text()').extract()[0].split()[1:])})

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
