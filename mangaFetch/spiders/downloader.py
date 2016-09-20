# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from mangaFetch.items import MangafetchItem

class DownloaderSpider(CrawlSpider):
    name = "downloader"
    
    def __init__(self,name=None):
        new_name = name.replace(' ','-')
        final_name = str(new_name.lower())
        self.allowed_domains = ["mangapanda.com",]
        self.start_urls = ('http://www.mangapanda.com/%s/1'%final_name,)


    def parse(self, response):
        item = MangafetchItem()
        mangaName = response.xpath(".//div[@id='mangainfo']/div[1]/h1/text()").extract()
        page = response.xpath(".//div[@id='mangainfo']/div[1]/span[@class='c1']/text()").extract()
        item['MangaName'] = response.xpath(".//div[@id='mangainfo']/div[2]/h2[@class='c2']/a/text()").extract()
        item['filename'] = mangaName
        item['title'] = [page[0] + mangaName[0]]
        item['image_urls'] = [response.xpath(".//img[@id='img']/@src").extract_first()]
        yield item
        next_page = response.xpath(".//*[@class='next']/a/@href").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)