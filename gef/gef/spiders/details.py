# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class DetailsSpider(CrawlSpider):
    name = "details"
    allowed_domains = ["www.thegef.org"]
    start_urls = ()

    def parse(self, response):
    	print(response)
    	pass

    def get_links_as_list():
    	f = open("links.txt", "r")
    	lines = f.read().split('\r\n')
    	return list(lines)

    start_urls = (get_links_as_list())