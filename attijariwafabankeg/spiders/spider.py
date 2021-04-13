import scrapy

from scrapy.loader import ItemLoader

from ..items import AttijariwafabankegItem
from itemloaders.processors import TakeFirst


class AttijariwafabankegSpider(scrapy.Spider):
	name = 'attijariwafabankeg'
	start_urls = ['https://www.attijariwafabank.com.eg/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="pop"]/@href').getall()
		print(len(post_links))
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@title="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time[@class="updated date-style"]/text()').get()

		item = ItemLoader(item=AttijariwafabankegItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
