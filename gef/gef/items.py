# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GefItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    project_title = scrapy.Field()
    project_summary = scrapy.Field()
    project_id = scrapy.Field()
    project_type = scrapy.Field()
    status = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    focal_areas = scrapy.Field()
    funding_source = scrapy.Field()
    implementing_agencies = scrapy.Field()
    executing_agencies = scrapy.Field()
    gef_period = scrapy.Field()
    approval_fiscal_year = scrapy.Field()
    project_preparation_grant_amount = scrapy.Field()
    gef_project_grant = scrapy.Field()
    co_financing_total = scrapy.Field()
    gef_agency_fees = scrapy.Field()
    total_cost = scrapy.Field()
    timeline = scrapy.Field()
    project_documents = scrapy.Field()
    pass

class DocumentItem(scrapy.Item):
	project_id = scrapy.Field()
	title = scrapy.Field()
	type = scrapy.Field()
	text = scrapy.Field()
	link =scrapy.Field()

class TimelineItem(scrapy.Item):
	project_id = scrapy.Field()
	title = scrapy.Field()
	date = scrapy.Field()