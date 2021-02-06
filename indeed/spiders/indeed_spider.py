from scrapy import Spider, Request
from indeed.items import IndeedItem
from urllib.parse import parse_qs, urljoin, urlparse


class IndeedSpider(Spider):
    name = 'indeed_spider'
    allowed_urls = ['https://www.indeed.com']
    start_urls = ['https://www.indeed.com/jobs?q=data+scientist&l=New+York%2C+NY&sort=date']

    def parse(self, response):
        url_pattern = self.start_urls[0] + '&start={}'
        urls = [url_pattern.format(i*10) for i in range(10)]

        for url in urls[:1]:
            yield Request(url=url, callback=self.parse_jobs_page)

    def parse_jobs_page(self, response):
        job_pattern = '//a[contains(@class,"jobtitle")]/@href'
        jobs = response.xpath(job_pattern).getall()

        for job in jobs:
            url = self.allowed_urls[0] + job
            yield Request(url=url, callback=self.parse_job_page)

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
        original_url = response.css('div#originalJobLinkContainer a').attrib['href']
        posted_when = response.css('div.jobsearch-JobMetadataFooter div::text').getall()[1]
        salary = response.css('div.jobsearch-JobDescriptionSection-sectionItem span').get()

        item = IndeedItem()

        response.meta['indeed_url'] = response.url
        response.meta['job_title'] = job_title
        response.meta['company_name'] = company_name
        response.meta['company_url'] = urljoin(company_url, urlparse(company_url).path)
        response.meta['company_reviews'] = company_reviews
        response.meta['job_location'] = job_location
        response.meta['job_description'] = job_description
        response.meta['posted_when'] = posted_when
        response.meta['salary'] = salary

        yield Request(url = original_url, callback=self.resolve_redirected_url, meta=response.meta)
        
    def resolve_redirected_url(self, response):
        original_url = response.url

        item = IndeedItem()

        item['indeed_url'] = response.meta['indeed_url']
        parsed = urlparse(response.meta['indeed_url'])
        item['indeed_job_key'] = parse_qs(parsed.query).get('jk')
        item['job_title'] = response.meta['job_title']
        item['company_name'] = response.meta['company_name']
        item['company_url'] = response.meta['company_url']
        item['company_reviews'] = response.meta['company_reviews']
        item['job_location'] = response.meta['job_location']
        item['job_description'] = response.meta['job_description']
        item['original_url'] = original_url
        item['posted_when'] = response.meta['posted_when']
        item['salary'] = response.meta['salary']

        yield item

        
