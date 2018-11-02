# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exceptions import DropItem

class DuplicatePhoneNumbersPipeline(object):
    def __init__(self):
        self.phone_numbers_seen = set()

    def process_item(self, item, spider):
        if item['phone_number'] in self.phone_numbers_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.phone_numbers_seen.add(item['phone_number'])
            return item

class ContactsPipeline(object):
    def process_item(self, item, spider):
        return item
