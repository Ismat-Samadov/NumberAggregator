import scrapy


class CollectorSpider(scrapy.Spider):
    name = "collector"
    allowed_domains = ["autonet.az"]
    start_urls = ["https://autonet.az"]

    def parse(self, response):
        pass
