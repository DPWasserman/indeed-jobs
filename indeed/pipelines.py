# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
import pandas as pd
import pymssql
import re

# class IndeedPipeline:
#     def process_item(self, item, spider):
#         return item

filename = 'indeed.csv'


class CleansePipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try:
            adapter['num_stars'], _, adapter['num_reviews'] = re.findall('([/d.]+)', adapter['company_reviews'])
        except:
            adapter['num_stars'] = None
            adapter['num_reviews'] = None

        if adapter['posted_when'] in ['Today', 'Just posted']:
            day_diff = 0
        else:
            try:
                day_diff = re.findall('/d+', adapter['posted_when'])
            except:
                day_diff = None


class DataPipeline(object):
    def __init__(self):
        self.conn = pymssql.connect(host='127.0.0.1', user='', password='', database='job_scraper')
        self.cursor = self.conn.cursor()
        self.filename = filename

    def process_item(self, item, spider):
        try:
            df = pd.read_csv(self.filename)
            company_df =  df[['company_name','company_url','num_stars','num_reviews']].unique()
            
            sql_statement = f'INSERT INTO jobs() VALUES ({item["text"]}, {item[""]}, {item[""]})'
            self.cursor.execute(sql_statement)
            self.conn.commit()
        except pymssql.Error as e:
            print ("error")

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['indeed_job_key'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['indeed_job_key'])
            return item

class WriteItemPipeline(object):

    def __init__(self):
        self.filename = filename

    def open_spider(self, spider):
        self.csvfile = open(self.filename, 'wb')
        self.exporter = CsvItemExporter(self.csvfile)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.csvfile.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
