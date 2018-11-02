import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from contacts.items import ContactsItem

class HarajComSaSpider(BaseSpider):
    name = 'haraj.com.sa'
    allowed_domains = ['haraj.com.sa']

    def start_requests(self):
        yield Request('http://haraj.com.sa/', callback=self.parse_menu)

    def parse_menu(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//div[@class="new_menu"]//a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_list)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//table[@class="front_table"]//td[@class="num"]/a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_ad)

        for url in hxs.select(u'//div[@class="pagination"]//a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_list)

    def parse_ad(self, response):
        hxs = HtmlXPathSelector(response)
        phone_number = re.search('(05\d{8})', response.body)
        if phone_number:
            item = ContactsItem()
            item['city'] = hxs.select(u'normalize-space(//a[starts-with(@href, "http://haraj.com.sa/city/")]/text())').extract()[0]
            item['phone_number'] = phone_number.groups()[0]
            yield item
        else:
            self.log('No phone number found on <%s>' % (response.url))
