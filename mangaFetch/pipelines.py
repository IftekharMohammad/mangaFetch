# # -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

class MangafetchPipeline(ImagesPipeline):

	def change_filename(self, key, response):
		return "%s/%s/%s.jpg"%(response.meta['MangaName'][0],response.meta['filename'][0],response.meta['title'][0])
        
	def get_media_requests(self, item, info):
		return [Request(x, meta={'title': item["title"],'filename': item["filename"],'MangaName': item["MangaName"]})
			for x in item.get('image_urls', [])]

	def get_images(self, response, request, info):
		for key, image, buf, in super(MangafetchPipeline, self).get_images(response, request, info):
			key = self.change_filename(key, response)
			yield key, image, buf
