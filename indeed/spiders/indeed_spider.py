from scrapy import Spider, Request
from indeed.items import IndeedItem
import datetime
import re
from urllib.parse import parse_qs, urljoin, urlparse
import logging

class IndeedSpider(Spider):
    name = 'indeed_spider'
    allowed_urls = ['https://www.indeed.com']
    start_urls = ['https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY&sort=date']

    def parse(self, response):
        url_pattern = self.start_urls[0] + '&start={}'
        urls = [url_pattern.format(i*10) for i in range(10)]

        for url in urls[:3]: # Parse first two pages only
            yield Request(url=url, callback=self.parse_jobs_page)

    def parse_jobs_page(self, response):
        job_pattern = '//a[contains(@class,"jobtitle")]/@href'
        jobs = response.xpath(job_pattern).getall()

        for job in jobs:
            url = self.allowed_urls[0] + job
            response.meta['search_page_url'] = response.url
            yield Request(url=url, callback=self.parse_job_page, meta=response.meta)

    def parse_job_page(self, response):
        job_title = response.css('h1.jobsearch-JobInfoHeader-title::text').get()

        company = response.css('div.jobsearch-DesktopStickyContainer-companyrating a')
        company_name = company.xpath('./text()').get()
        company_url = company.xpath('./@href').get()
        company_reviews = response.css('div.icl-Ratings-starsCountWrapper').xpath('@aria-label').get()
        
        if not company_name:
            company_name = response.css('div.jobsearch-JobInfoHeader-subtitle div.jobsearch-InlineCompanyRating div::text').get()

        job_location = response.css('div.jobsearch-JobInfoHeader-subtitle div::text').getall()[-1]
        job_description_texts = response.css('div#jobDescriptionText').xpath('.//text()').getall()
        job_description = ''.join(job_description_texts)

        posted_when_block = response.css('div.jobsearch-JobMetadataFooter div::text').getall()
        posted_when = None
        for post in posted_when_block:
            posted_when = re.findall(r'(Just posted|\d+ day[s]* ago)', post)
            if posted_when:
                posted_when = posted_when[0]
                break

        salary = response.css('div.jobsearch-JobDescriptionSection-sectionItem span').xpath('.//text()').get()

        original_url = response.css('div#originalJobLinkContainer a').xpath('./@href').get()

        response.meta['indeed_url'] = response.url
        response.meta['job_title'] = job_title
        response.meta['company_name'] = company_name
        response.meta['company_url'] = urljoin(company_url, urlparse(company_url).path)
        response.meta['company_reviews'] = company_reviews
        response.meta['job_location'] = job_location
        response.meta['job_description'] = job_description
        response.meta['posted_when'] = posted_when
        response.meta['salary'] = salary

        if original_url:
            yield Request(url=original_url, callback=self.resolve_redirected_url, meta=response.meta)
        else: # Sometimes there is no original post link
            response.meta['original_url'] = response.url
            yield self.store_item(response.meta)            


    def resolve_redirected_url(self, response): 
        response.meta['original_url'] = response.url
        yield self.store_item(response.meta)


    def store_item(self, data_dict):
        item = IndeedItem()

        # Raw scraped information
        item['search_page_url'] = data_dict['search_page_url']
        item['indeed_url'] = data_dict['indeed_url']
        item['job_title'] = data_dict['job_title']
        item['company_name'] = data_dict['company_name']
        item['company_url'] = data_dict['company_url']
        item['company_reviews'] = data_dict['company_reviews']
        item['job_location'] = data_dict['job_location']
        item['job_description'] = data_dict['job_description']
        item['original_url'] = data_dict['original_url']
        item['posted_when'] = data_dict['posted_when']
        item['salary'] = data_dict['salary']

        # Calculated information
        parsed = urlparse(data_dict['indeed_url'])
        item['indeed_job_key'] = parse_qs(parsed.query).get('jk')[0]

        if data_dict['company_reviews']:
            num_stars, _, num_reviews = re.findall(r'^([\d.]+) out of (\d) from ([\d,]+) employee rating', data_dict['company_reviews'])[0]
            item['num_stars'] = float(num_stars)
            item['num_reviews'] = int(num_reviews.replace(',',''))

        if data_dict['salary']:
            salary_range = re.findall(r'\$([\d,]+)', data_dict['salary'])
            job_salary_low = salary_range[0]
            job_salary_high = salary_range[-1]
            item['job_salary_low'] = int(job_salary_low.replace(',',''))
            item['job_salary_high'] = int(job_salary_high.replace(',',''))

        if data_dict['posted_when']:
            if data_dict['posted_when'] == 'Just posted':
                days_ago = 0
            else:
                days_ago = int(re.findall(r'(\d+)', data_dict['posted_when'])[0])
            post_date = datetime.datetime.now() - datetime.timedelta(days = days_ago)
            item['post_date'] = post_date.date()

        return item
