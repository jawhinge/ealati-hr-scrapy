import scrapy
from ..items import ScrapyEalatihrItem
from scrapy.http.request import Request
from datetime import datetime,timezone

class EalatihrSpider(scrapy.Spider):
    name = 'ealatihr'
    allowed_domains = ['ealati.hr']

    def start_requests(self):
        yield Request(url = "https://www.ealati.hr/", callback = self.parse_categories)

    def parse_categories(self, response):
        for link in response.css('#menu-footer-widget-izbornik-desno a::attr(href)').extract():
            yield response.follow(link, callback = self.parse) 


    def parseItem(self, response):
        item = ScrapyEalatihrItem()
        item['productUrl'] = response.url
        item['listingUrl'] = response.meta.get('url')
        item['sku'] = response.xpath('//span[@class="sku"]/text()').extract()[0]
        item['name'] = response.xpath('//*[@id="content"]/div/nav/text()').extract()[0]
        item['category'] = response.xpath('//*[@class="woocommerce-breadcrumb"]//text()').extract()[1:-1]
        response.xpath('//span[@class="tagged_as"]/a/text()').extract()[0]        
        item['price'] = response.xpath('//p[@class="price"]//text()').extract()[0]

        if response.xpath('//p[@class="price"]/span/del') != []:
            item['oldPrice'] = response.xpath('//p[@class="price"]/span/del//text()').extract()[0]

        if  response.xpath('//figure[@class="electro-wc-product-gallery__wrapper"]/figure/a/@href').extract() != []:
            item['images'] = response.xpath('//figure[@class="electro-wc-product-gallery__wrapper"]/figure/a/@href').extract()
        else:
            response.xpath('//figure[@class="woocommerce-product-gallery__wrapper"]/div/a/@href').extract()[0]

        specsRaw = response.xpath('//div[@class="ealati_specifikacija"]/p//text()').extract()
        specs = []
        for spec in specsRaw:
            specs.append(spec.strip())

        item['specsTable'] = self.Convert(specs)
        now_utc = datetime.now(timezone.utc)
        item['crawledAt'] = str(now_utc).split('.')[0]

        yield item



    def parse(self, response):

        for link in response.css('a.woocommerce-loop-product__link::attr(href)').extract():
            yield response.follow(link, callback=self.parseItem, meta={'url': response.url})

        
        next_page = response.css('a.next.page-numbers')
        if next_page != []:
            yield response.follow(next_page.attrib['href'], callback=self.parse)

    def Convert(self, list):
        table = []
        for i,k in zip(list[0::2], list[1::2]):
            table.append({'key':str(i), 'value':str(k)})
        return table