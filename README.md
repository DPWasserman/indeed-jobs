# Scraping of Data Science Job Postings on Indeed.com
## Project Background
The goal of any job seeker is to land a position. Data science is a very hot area for job prospects. Thus, there are a number of positions open and a number of seekers looking to fill those positions.
The aim of this project is to assist job seekers by analyzing Data Scientist job postings on Indeed.com in 6 different cities across the United States. Those cities are: 
- **Charlotte, NC**
- **Chicago, IL**
- **Los Angeles, CA**
- **New York, NY**
- **Phoenix, AZ**
- **San Francisco, CA**

Additional cities for later consideration:
- Atlanta, GA
- Austin, TX
- Boston, MA
- Seattle, WA
- Washington, DC

For detailed insights, please see the PPTX file in this repo.

## How to Run the Scraper
1. Enter in the desired locations and a desirable proxy in the `config.py` file in the `indeed` sub-folder
    - For a good, free proxy, refer to https://www.us-proxy.org/
2. Run the main scraper to get the job postings: `scrapy crawl indeed_spider`
    - Results will be placed in the `data` sub-folder as `indeed_spider.csv`
3. Run the secondary scraper to resolve the original posting URL: `scrapy crawl redirect_spider`
    - Results will be placed in the `data` sub-folder as `redirect_spider.csv`
4. Open the three Jupyter Notebooks to analyze the results:
    - **Job_Description_Word_Cloud.ipynb** : Produces a na&#239;ve word cloud
    - **Job_Statistics_Calculations.ipynb** : Produces statistical analysis from posting metadata
    - **Job_Text_Analysis.ipynb** : Produces analysis from natural language processing from the job descriptions
