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
    image_url = scrapy.Field()
 
class ProductsItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price_euros = scrapy.Field()
    price_cents = scrapy.Field()
    price_concat = scrapy.Field()
    product_id = scrapy.Field()
    product_code = scrapy.Field()
    product_category = scrapy.Field()
    description = scrapy.Field()  
