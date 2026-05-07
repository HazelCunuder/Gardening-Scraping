# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from dotenv import load_dotenv
from .database import get_session
from .items import CategoryItem, ProductsItem
from .models import Category, Product

load_dotenv()

# les noms des champs doivent être les mêmes des deux côtés
ITEM_MODEL_MAP = {
    CategoryItem: Category,
    ProductsItem: Product,
}

class GardeningScraperPipeline:
    def process_item(self, item, spider):
        return item

class PostgreSQLPipeline:

    def __init__(self):
        self.session = None

    def open_spider(self, spider):
        self.session = get_session()
        spider.logger.info("Connexion PostgreSQL établie.")

    def process_item(self, item, spider):
        model_class = ITEM_MODEL_MAP.get(type(item))

        if model_class is None:
            spider.logger.warning(f"Item non géré : {type(item).__name__}")
            return item

        instance = model_class(**{
            k: item.get(k) for k in item.fields
        })

        self.session.add(instance)
        self.session.commit()
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
        spider.logger.info("Connexion PostgreSQL fermée.")


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
    