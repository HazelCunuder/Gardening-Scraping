import scrapy
from gardening_scraper.items import ProductsItem

class PagelistSpiderSpider(scrapy.Spider):
    name = "pagelist_spider"
    custom_settings = {
        "ITEM_PIPELINES" : {
            'gardening_scraper.pipelines.ProductPipeline' : 400
        }
    }
    allowed_domains = ["www.bricodepot.fr"]
    start_urls = ["https://www.bricodepot.fr/produits/cuisine/electromenager-et-equipement-de-cuisine/electromenager/petit-electromenager"]

    def parse(self, response):
        products = response.css("div.plp-products-grid article.product-card")

        for product in products:
            relative_url = product.css("a.product-card-link ::attr(href)").get()
            product_url = "https://www.bricodepot.fr"+relative_url
            yield response.follow(product_url, callback= self.parse_product_page)

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
