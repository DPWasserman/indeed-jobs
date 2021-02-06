# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class IndeedItem(scrapy.Item):
    indeed_url = scrapy.Field()
    indeed_job_key = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_reviews = scrapy.Field()
    job_location = scrapy.Field()
    job_description = scrapy.Field()
    original_url = scrapy.Field()
    posted_when = scrapy.Field()
