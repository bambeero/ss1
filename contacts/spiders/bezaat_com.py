import re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from contacts.items import ContactsItem

class BezaatComSpider(BaseSpider):
    name = 'bezaat.com'
    allowed_domains = ['bezaat.com']

    def start_requests(self):
        yield Request('http://bezaat.com/ksa/riyadh', callback=self.parse_cities)

    def parse_cities(self, response):
        hxs = HtmlXPathSelector(response)

        for city in hxs.select(u'//div[@id="selectableCities"]//a'):
            url = urljoin_rfc(get_base_url(response), city.select(u'./@href').extract()[0])
            yield Request(url, callback=self.parse_menu,
                    meta={'city': city.select(u'./@title').extract()[0]})

    def parse_menu(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//div[@id="rightBlock"]//a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_list, meta=response.meta)

    def parse_list(self, response):
        hxs = HtmlXPathSelector(response)

        for url in hxs.select(u'//div[contains(@class, "description")]//h2/a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_ad, meta=response.meta)

        for url in hxs.select(u'//ul[@class="pagination"]//a/@href').extract():
            url = urljoin_rfc(get_base_url(response), url)
            yield Request(url, callback=self.parse_list, meta=response.meta)

    def parse_ad(self, response):
        hxs = HtmlXPathSelector(response)
        phone_number = re.search('(05\d{8})', response.body)
        if phone_number:
            item = ContactsItem()
            item['city'] = response.meta['city']
            item['phone_number'] = phone_number.groups()[0]
            yield item
        else:
            self.log('No phone number found on <%s>' % (response.url))
