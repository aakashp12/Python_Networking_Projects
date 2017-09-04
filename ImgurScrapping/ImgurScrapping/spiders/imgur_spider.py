import scrapy

from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from ImgurScrapping.items import ImgurscrappingItem

class ImgurScrappingSpider(CrawlSpider):
	name = 'ImgurScrapping'
	allowed_domains = ['imgur.com']
	start_urls = ['http://www.imgur.com']
	rules = [Rule(LinkExtractor(allow=['/gallery/.*']), 'parse_imgur')]

	def parse_imgur(self, response):
		image = ImgurscrappingItem()
		image['title'] = response.xpath(\
				"//h1/text()").extract()
		relative_address = response.xpath("//img/@src").extract()
		image['image_urls'] = ['http:' + relative_address[0]]
		return image
	
