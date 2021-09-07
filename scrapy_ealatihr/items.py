# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyEalatihrItem(scrapy.Item):
    # define the fields for your item here like:
    productUrl = scrapy.Field()
    listingUrl = scrapy.Field()
    sku = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    price = scrapy.Field()
    oldPrice = scrapy.Field()
    images = scrapy.Field()
    specsTable = scrapy.Field()
    crawledAt = scrapy.Field()
    
    pass
