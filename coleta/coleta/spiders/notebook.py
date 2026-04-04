import scrapy


class TecladoSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook?sb=all_mercadolibre#D[A:notebook]"]

    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')
    
        for product in products:
         
            yield {
                'seller': product.css('span.poly-component__seller::text').get(),       
                'name': product.css('a.poly-component__title::text').get(),
            }
