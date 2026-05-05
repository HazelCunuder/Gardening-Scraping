import scrapy


class PagelistSpiderSpider(scrapy.Spider):
    name = "pagelist_spider"
    allowed_domains = ["www.bricodepot.fr"]
    start_urls = ["https://www.bricodepot.fr/"]

    def parse(self, response):
        pass
