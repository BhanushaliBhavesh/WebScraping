#Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):


        adpater = ItemAdapter(item)
        c_names = adpater.field_names()
       
        for c_name in c_names:
            

            if c_name != 'description':

                value = adpater.get(c_name)
                adpater[c_name] = value.strip()
        return item



