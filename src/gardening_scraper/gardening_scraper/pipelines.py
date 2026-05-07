# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter


class GardeningScraperPipeline:
    def process_item(self, item, spider):
        return item

class ProductPipeline:
    def process_item(self, item, spider):
        # Strip whitespace from all string fields
        for field in item:
            if isinstance(item[field], str):
                item[field] = item[field].strip()

        # price_concat
        if item.get('price_concat'):
            try:
                item['price_concat'] = float(item['price_concat'].replace('€', '.'))
            except (ValueError, AttributeError):
                item['price_concat'] = None

        # product_id
        if item.get('product_id'):
            try:
                item['product_id'] = int(re.sub(r'\D', '', item['product_id']))
            except (ValueError, AttributeError):
                item['product_id'] = None

        # product_code
        if item.get('product_code'):
            try:
                item['product_code'] = int(re.sub(r'\D', '', item['product_code']))
            except (ValueError, AttributeError):
                item['product_code'] = None

        return item
    