import scrapy
from gardening_scraper.items import CategoryItem

class CategoryspiderSpider(scrapy.Spider):
    name            = "categories"
    allowed_domains = ["bricodepot.fr"]
    start_urls      = ["https://www.bricodepot.fr/produits"]

    custom_settings = {
        'FEEDS': {
            'categories.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    def parse(self, response, parent_category="Home"):
        categories = response.css('li.plp-univers-subcategory-list-item')

        if categories:
            for category in categories:
                category_item = CategoryItem()
                
                name = category.css('a.plp-univers-subcategory-title::text').get()
                cat_url  = "https://www.bricodepot.fr" + category.css('a.plp-univers-subcategory-title::attr(href)').get()

                category_item['category_name']   = name
                category_item['url']             =  cat_url
                # category_item['category_id']     = id
                category_item['parent_category'] = parent_category
                yield category_item

                yield response.follow(cat_url, callback  = self.parse, cb_kwargs = {'parent_category': name})
        else:
            yield from self.parse_products(response)
    
    def parse_product(self, response):
        pass
