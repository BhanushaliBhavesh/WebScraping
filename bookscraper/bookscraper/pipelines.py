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
    


