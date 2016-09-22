# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.spiders import CrawlSpider
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

class ChapterDownloadSpider(scrapy.Spider):
    name = "chapterDownload"

    def __init__(self,name=None,chapter=None):
        new_name = name.replace(' ','-')
        global final_name
        final_name = str(new_name.lower())
        global chapter_no
        chapter_no = chapter
        self.allowed_domains = ["mangapanda.com",]
        self.start_urls = ('http://www.mangapanda.com/%s/%s'%(final_name,chapter_no),)

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
            chapter_finder = r"^https?\:\/\/([^\/:?#]+)(?:[\/:?#]|$)"+re.escape(final_name)+"/"+re.escape(chapter_no)+"/"+r"[0-9]+"
            if(re.search(chapter_finder,next_page,re.IGNORECASE)):
                 yield scrapy.Request(next_page, callback=self.parse)