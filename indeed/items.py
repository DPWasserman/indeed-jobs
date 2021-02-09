# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class IndeedItem(scrapy.Item):
    # Scraped in Spider
    search_page_url = scrapy.Field()
    indeed_url = scrapy.Field()
    job_title = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    company_reviews = scrapy.Field()
    job_location = scrapy.Field()
    job_description = scrapy.Field()
    original_url = scrapy.Field()
    posted_when = scrapy.Field()
    salary = scrapy.Field()

    # Created from Scraped Data
    search_location = scrapy.Field()
    indeed_job_key = scrapy.Field()
    num_stars = scrapy.Field()
    num_reviews = scrapy.Field()
    job_salary_low = scrapy.Field()
    job_salary_high = scrapy.Field()
    post_date = scrapy.Field()
