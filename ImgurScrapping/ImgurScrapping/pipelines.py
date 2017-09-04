# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline

class ImgurscrappingPipeline(ImagesPipeline):
    
	def set_filename(self, response):
		# add a regex here to check is valid
		return 'full/{0}.jpg'.format(response.meta['title'][0])
	
	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url,\
					meta={'title': item['title']})
	
	def get_images(self, response, request, info):
		for key, image, buf in super(ImgurscrappingPipeline, self).get_images(\
									response, request, info):
			key = self.set_filename(response)
		yield key, image, buf

