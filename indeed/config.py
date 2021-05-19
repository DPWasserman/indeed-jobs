"""
This file is for configuration variables such as locations to scrape and the proxy to use.
"""
JOB_QUERY = 'data scientist' # Job to be searched

LOCATIONS = ('New York, NY',
             'San Francisco, CA',
             'Los Angeles, CA',
             'Chicago, IL',
             'Phoenix, AZ',
             'Charlotte, NC',
             'Boston, MA',
             'Austin, TX',
             'Seattle, WA',
             'Washington, DC',
             'Atlanta, GA'
            )  # Inspired by https://www.datascienceweekly.org/articles/where-are-data-science-jobs-located

PROXY = '208.80.28.208:8080'
 # Chosen from https://free-proxy-list.net/
 # Ensure that Country is United States, HTTPS is allowed (YES), and Anonymity is set to Elite Proxy
