# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    stars = scrapy.Field()
    product_description = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    price_execluding_tax = scrapy.Field()
    price_including_tax = scrapy.Field()
    tax = scrapy.Field()
    availablity = scrapy.Field()
    number_of_reviews = scrapy.Field()