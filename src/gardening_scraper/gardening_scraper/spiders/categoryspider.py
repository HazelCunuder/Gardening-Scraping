import scrapy
from gardening_scraper.gardening_scraper.items import CategoryItem

class CategoryspiderSpider(scrapy.Spider):
    name            = "categories"
    allowed_domains = ["bricodepot.fr"]
    start_urls      = ["https://www.bricodepot.fr/produits"]

    custom_settings = {
        'FEEDS': {
            'categories.csv': {'format': 'csv', 'overwrite': True}
        },
        "ITEM_PIPELINES": {
            'gardening_scraper.gardening_scraper.pipelines.GardeningScraperPipeline': 100,
            'gardening_scraper.gardening_scraper.pipelines.PostgreSQLPipeline': 300,
        }
    }

    def parse(self, response):
        categories = response.css('li.plp-univers-subcategory-list-item')
        filters = ["modele","premier-prix", "1er-prix","promo","offres","promotion","occasion","soldes","bons-plans", "actu", "actualites"]

        if categories:
            for category in categories:
                category_item = CategoryItem()

                cat_url  = "https://www.bricodepot.fr" + category.css('a.plp-univers-subcategory-title::attr(href)').get()

                real_category = True
                for word in filters:
                    if word in cat_url:
                        real_category = False
                        break

                if real_category:
                    category_item['category_name']   = category.css('a.plp-univers-subcategory-title::text').get()
                    category_item['url']             = cat_url
                    category_item['category_id']     = cat_url.split('/')[-1]
                    category_item['parent_category'] = response.url.split('/')[-1]
                    category_item['image_url'] = category.css('img::attr(src)').get()
                    yield category_item

                    yield response.follow(cat_url, callback  = self.parse)
                    break # à effacer ou commenter pour récuperer toutes les catégories
