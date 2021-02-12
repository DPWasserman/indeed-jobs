# Analysis of Data Science Job Postings on Indeed.com
## Project Background
The goal of any job seeker is to land a position. Data science is a very hot area for job prospects. Thus, there are a number of positions open and a number of seekers looking to fill those positions.
The aim of this project is to assist job seekers by analyzing Data Scientist job postings on Indeed.com in 11 different cities across the United States. Those cities are: 
- Atlanta, GA
- Austin, TX
- Boston, MA
- Charlotte, NC
- Chicago, IL
- Los Angeles, CA
- New York, NY
- Phoenix, AZ
- San Francisco, CA
- Seattle, WA
- Washington, DC

For detailed insights, please see the Jupyter Notebooks in this repo.

## Setup Instructions
1. Enter in the desired locations and a desirable proxy in the config.py file in the indeed sub-folder
    - For a good, free proxy, refer to https://www.us-proxy.org/
2. Run the main scraper to get the job reqs: scrapy crawl indeed_spider
    - Results will be placed in the data sub-folder as indeed_spider.csv
3. Run the secondary scraper to resolve the original posting URL: scrapy crawl redirect_spider
    - Results will be placed in the data sub-folder as redirect_spider.csv
4. Open the two Jupyter Notebooks to see the analysis:
    - Job_Description_Analysis.ipynb
    - Job_Analysis.ipynb