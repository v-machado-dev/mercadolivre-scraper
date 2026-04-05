import scrapy


class TecladoSpider(scrapy.Spider):
    name = "notebook"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/notebook?sb=all_mercadolibre_Desde_1"]
    page_count = 1
    max_page = 10

    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')
    
        for product in products:
        
            yield {
            'seller': product.css('span.poly-component__seller::text').get(),       
            'name': product.css('a.poly-component__title::text').get(),
            'avg_review': product.css('span.poly-component__review-compacted span.poly-phrase-label::text').get(),
            'old_price': product.css('div.poly-component__price s span.andes-money-amount__fraction::text').get(),
            'new_price': product.css('div.poly-price__current span.andes-money-amount__fraction::text').get(),
        }

        if self.page_count < self.max_page:
            next_from = 1 + (self.page_count * 48)
            next_page = f"https://lista.mercadolivre.com.br/notebook?sb=all_mercadolibre_Desde_{next_from}"
            self.page_count += 1
            yield scrapy.Request(url=next_page, callback=self.parse)
