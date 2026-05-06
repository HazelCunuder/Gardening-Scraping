import scrapy
import json
import math
from gardening_scraper.items import ProductsItem

class PagelistSpiderSpider(scrapy.Spider):
    name = "pagelist_spider"
    custom_settings = {
        "ITEM_PIPELINES" : {
            'gardening_scraper.pipelines.ProductPipeline' : 400
        }
    }
    allowed_domains = ["www.bricodepot.fr"]
    start_urls = ["https://www.bricodepot.fr/produits/carrelage-stratifie-et-parquet/stratifie-parquet-et-sol-vinyle-pvc/sol-stratifie"]

    def parse(self, response):
        for script in response.css('script::text').getall():
            script = script.strip()
            if '"ItemList"' not in script or 'itemListElement' not in script:
                continue
            
            data = json.loads(script)
            products = data.get('itemListElement', [])
            total_products = data.get('numberOfItems')
            products_per_page = len(products)
            current_page = response.meta.get('page', 1)
    
            self.logger.info(f"Page {current_page}: {products_per_page} products, total={total_products}, last_page={math.ceil(total_products / products_per_page) if total_products and products_per_page else 'unknown'}")
    
            for entry in products:
                product = entry.get('item', {})
                product_url = product.get('url')
                if product_url:
                    yield response.follow(product_url, callback=self.parse_product_page)
    
            if total_products and products_per_page:
                last_page = math.ceil(total_products / products_per_page)
                if current_page < last_page:
                    yield response.follow(
                        f"{self.start_urls[0]}/{current_page + 1}",
                        callback=self.parse,
                        meta={'page': current_page + 1}
                    )
            break

    def parse_product_page(self,response):
        product_item = ProductsItem()

        product_item['url'] = response.url
        product_item['name'] = response.css("h1 ::text").get()
        product_item['price_euros'] = response.css("p.product-price-tag span ::text").get()
        product_item['price_cents'] = response.css("p.product-price-tag sup ::text").get()
        product_item['price_concat'] = product_item['price_euros']+product_item['price_cents']
        product_item['product_id'] = response.css("div.pdp-info-modal p.pdp-info-modal-ref small:nth-child(1)::text").get()
        product_item['product_code'] = response.css("div.pdp-info-modal p.pdp-info-modal-ref small:nth-child(2)::text").get()
        product_item['product_category'] = response.css("ol.breadcrumbs-list li.breadcrumbs-list-item:nth-last-child(2) a ::text").get()
        product_item['description'] = " ".join(response.css("div.pdp-info-modal-section.pdp-info-modal-description *::text").getall())

        yield product_item
