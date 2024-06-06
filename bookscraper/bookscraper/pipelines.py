#Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


def string_cleaner(rouge_text):
  
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', rouge_text)
    return cleaned_text

class BookscraperPipeline:
    def process_item(self, item, spider):


        adpater = ItemAdapter(item)
        c_names = adpater.field_names()
              
        for c_name in c_names:
            

            if c_name != 'description':

                value = adpater.get(c_name)
                adpater[c_name] = string_cleaner(value)



        signs = ['price_execluding_tax', 'price_including_tax', 'tax']

        for sign in signs:

            value = string_cleaner(adpater.get(sign))
            print("printing the value -------------", value)
            adpater[sign] = value

        
        availablity = adpater.get('availablity')
        value = availablity.split('(')[1].split(' ')[0]
        adpater['availablity'] = value[0]


        stars = adpater.get('stars')
        value = stars.split(' ')[1].lower()
        
        stars_rating = {

            'one' : 1,
            'two' : 2,
            'three': 3,
            'four': 4,
            'five': 5,

        }

        adpater['stars'] = stars_rating[value]


        return item
    

import mysql.connector
import os

class SaveToMySQLPipeline:

    def __init__(self):
        mysql_password = os.getenv('MYSQL_PASSWORD')
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password=mysql_password,
            database = 'books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_execluding_tax DECIMAL,
            price_including_tax DECIMAL,
            tax DECIMAL,
            availablity INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        ## Define insert statement
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_execluding_tax,
            price_including_tax,
            tax,
            availablity,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_execluding_tax"],
            item["price_including_tax"],
            item["tax"],
            item["availablity"],
            item["number_of_reviews"],
            item["stars"],
            item["category"],
            str(item["product_description"])
        ))

        # ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()