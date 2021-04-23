import scrapy


class BankalbiladItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
