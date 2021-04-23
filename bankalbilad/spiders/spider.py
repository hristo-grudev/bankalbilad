import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import BankalbiladItem
from itemloaders.processors import TakeFirst


class BankalbiladSpider(scrapy.Spider):
	name = 'bankalbilad'
	start_urls = ['https://www.bankalbilad.com/_LAYOUTS/15/BAB.V2.Internet.Web/web/api.aspx?Operation=getnews&lang=ar&IgnoreCache=false']

	def parse(self, response):
		data = response.text
		post_links = re.findall(r'<Item>(.*?)</Item>', data, re.DOTALL)
		for post in post_links:
			url = re.findall(r'<URL>(.*?)</URL>', post, re.DOTALL)[0]
			date = re.findall(r'<Date>(.*?)</Date>', post, re.DOTALL)
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h2[@class="content-head"]//text()[normalize-space()]').get()
		description = response.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01__ControlWrapper_RichHtmlField"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BankalbiladItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		yield item.load_item()
