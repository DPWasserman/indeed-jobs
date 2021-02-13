import datetime
import pandas as pd
import re
from urllib.parse import quote_plus, parse_qs, unquote, urljoin, urlparse
import logging

from scrapy import Spider, Request
from indeed.items import IndeedItem, RedirectItem
from indeed import config


class IndeedSpider(Spider):
    name = 'indeed_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
        'indeed.pipelines.DuplicatesPipeline': 250,
        'indeed.pipelines.WriteItemPipeline': 300,
        }
    }

    primary_domain = 'https://www.indeed.com'

    def start_requests(self):
        url_pattern = 'https://www.indeed.com/jobs?q=data+scientist&l={}&sort=date'
        urls = [url_pattern.format(quote_plus(location)) for location in config.LOCATIONS]

        for url in urls:
            yield Request(url=url, callback=self.parse_results_page, meta={'proxy':config.PROXY}, dont_filter=True)
        

    def parse_results_page(self, response):
        if self.check_captcha(response):
            logging.error(f'CAPTCHA detected at {response.url}\nRetrying!')
            return None

        job_pattern = '//a[contains(@class,"jobtitle")]/@href'
        jobs = response.xpath(job_pattern).getall()

        for job in jobs:
            url = self.primary_domain + job
            response.meta['search_page_url'] = response.url
            yield Request(url=url, callback=self.parse_job_page, meta=response.meta)
        
        url = response.xpath('//a[@aria-label="Next"]/@href').get()
        if url:
            url = self.primary_domain + url
            yield Request(url=url, callback=self.parse_results_page)
    
    def parse_job_page(self, response):
        job_title = response.css('h1.jobsearch-JobInfoHeader-title::text').get()

        company = response.css('div.jobsearch-DesktopStickyContainer-companyrating a')
        company_name = company.xpath('./text()').get()
        company_url = company.xpath('./@href').get()
        company_reviews = response.css('div.icl-Ratings-starsCountWrapper').xpath('@aria-label').get()
        
        if not company_name:
            company_name = response.css('div.jobsearch-JobInfoHeader-subtitle div.jobsearch-InlineCompanyRating div::text').get()

        try:
            job_location = response.css('div.jobsearch-JobInfoHeader-subtitle div::text').getall()[-1]
        except:
            job_location = 'None posted'

        job_description_texts = response.css('div#jobDescriptionText').xpath('.//text()').getall()
        job_description = ''.join(job_description_texts)

        posted_when_block = response.css('div.jobsearch-JobMetadataFooter div::text').getall()
        posted_when = None
        for post in posted_when_block:
            posted_when = re.findall(r'(Just posted|Today|\d+[+]* day[s]* ago)', post)
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
            response.meta['original_url'] = original_url
        else:
            response.meta['original_url'] = None
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
        parsed = urlparse(data_dict['search_page_url'])
        item['search_location'] = unquote(parse_qs(parsed.query).get('l')[0])

        parsed = urlparse(data_dict['indeed_url'])
        try:
            item['indeed_job_key'] = parse_qs(parsed.query).get('jk')[0]
        except (TypeError, KeyError): 
            logging.error(f'Problem with {data_dict["indeed_url"]}')

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
            if data_dict['posted_when'] in ['Just posted','Today']:
                days_ago = 0
            else:
                days_ago = int(re.findall(r'(\d+)', data_dict['posted_when'])[0])
            post_date = datetime.datetime.now() - datetime.timedelta(days = days_ago)
            item['post_date'] = post_date.date()

        return item

    def check_captcha(self, response):
        """ Function that checks to see if a CAPTCHA is in use in the page """
        title = response.xpath('//title/text()').get()
        return 'Captcha' in title


class RedirectSpider(Spider):
    name = 'redirect_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
        'indeed.pipelines.WriteItemPipeline': 300,
        }
    }

    def start_requests(self):
        results_df = pd.read_csv('indeed_spider.csv')
        crawl = (np.logical_not(results_df['original_url'].isna()))
        urls = results_df.loc[crawl, 'original_url']

        for url in urls:
            yield Request(url=url, callback=self.follow_redirect, meta={'original_url':url, 'proxy':config.PROXY})

    def follow_redirect(self, response):
        redirected_url = response.url

        item = RedirectItem()
        item['original_url'] = response.meta['original_url']
        item['redirected_url'] = redirected_url
        yield item