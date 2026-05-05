# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GardeningScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductsItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    price_euros = scrapy.Field()
    price_cents = scrapy.Field()
    product_id = scrapy.Field()
    product_code = scrapy.Field()
    product_category = scrapy.Field()
    promotions = scrapy.Field()
        