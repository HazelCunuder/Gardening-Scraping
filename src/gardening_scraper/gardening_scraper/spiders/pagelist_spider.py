import scrapy

class PagelistSpiderSpider(scrapy.Spider):
    name = "pagelist_spider"
    allowed_domains = ["www.bricodepot.fr"]
    start_urls = ["https://www.bricodepot.fr/produits/cuisine/electromenager-et-equipement-de-cuisine/electromenager/petit-electromenager"]

    def parse(self, response):
        products = response.css("div.plp-products-grid article.product-card")

        for product in products:
            yield{
                'product-name': product.css("figure.product-card-figure figcaption.product-card-figcaption p.product-card-title ::text").get(),
                'url' : product.css("a.product-card-link ::attr(href)").get(),
                'price-euros' : product.css('figure.product-card-figure figcaption.product-card-figcaption div.product-price div.product-price-wrapper p.product-price-tag span ::text').get(),
                'price-cents': product.css('figure.product-card-figure figcaption.product-card-figcaption div.product-price div.product-price-wrapper p.product-price-tag sup ::text').get(),
            }

        #    relative_url = product.css("a.product-card-link ::attr(href)").get()
        #
        #    product_url = "https://www.bricodepot.fr/"+relative_url
        #
        #    yield response.follow(product_url, callback= self.parse_product_page)