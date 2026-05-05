# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GardeningScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    url = scrapy.Field()
    category_id = scrapy.Field()
    parent_category = scrapy.Field()
    
