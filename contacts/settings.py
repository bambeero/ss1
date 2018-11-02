# Scrapy settings for contacts project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'contacts'

SPIDER_MODULES = ['contacts.spiders']
NEWSPIDER_MODULE = 'contacts.spiders'

ITEM_PIPELINES = [
    'contacts.pipelines.DuplicatePhoneNumbersPipeline',
]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'contacts (+http://www.yourdomain.com)'
