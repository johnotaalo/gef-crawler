# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from gef.items import GefItem,DocumentItem, TimelineItem
import json


class ProjectsSpider(CrawlSpider):
    name = "projects"
    allowed_domains = ["www.thegef.org"]
    start_urls = (
        'http://www.thegef.org/projects-faceted?f[]=field_p_implagencies:170',
    )

    needed_urls = (
        'https://www.thegef.org/project/national-communications-unfccc',
        'https://www.thegef.org/project/national-capacity-self-assessment-ncsa-global-environmental-management-south-sudan',
        'https://www.thegef.org/project/initial-national-communication-unfccc',
        'https://www.thegef.org/project/preparations-national-adaptation-plan-action-napa-response-climate-change',
        'https://www.thegef.org/project/national-biodiversity-planning-support-implementation-cbd-2011-2020-strategic-plan-south-0',
        'https://www.thegef.org/project/gef-support-unccd-2018-national-reporting-process-umbrella-iv',
        'https://www.thegef.org/project/national-communications-programme-climate-change'
    )

    rules = (
    	Rule(
    		LinkExtractor(
    			allow=(),
    			restrict_xpaths=('.//li[@class="pager-last"]/a'),
    			process_value='clean_url'
    		),
    		callback="parse_item",
    		follow=True
    	),
    )

    def parse_item(self, response):
    	print('Processing...' + response.url)
    	# links = response.css('table.views-table > tbody > tr > td.views-field-title >a::attr(href)').extract()
    	links = ('https://www.thegef.org/project/national-communications-unfccc','https://www.thegef.org/project/national-capacity-self-assessment-ncsa-global-environmental-management-south-sudan', 'https://www.thegef.org/project/initial-national-communication-unfccc','https://www.thegef.org/project/preparations-national-adaptation-plan-action-napa-response-climate-change','https://www.thegef.org/project/national-biodiversity-planning-support-implementation-cbd-2011-2020-strategic-plan-south-0','https://www.thegef.org/project/gef-support-unccd-2018-national-reporting-process-umbrella-iv','https://www.thegef.org/project/national-communications-programme-climate-change')
    	f = open("links.txt", "a")
    	for a in links:
            print(a + "\n")
            yield scrapy.Request(a, callback=self.parse_detail_page)
    	pass

    def parse_detail_page(self, response):
    	project_title = response.css('div.title-area h1::text').extract()[0].strip()
    	project_summary = response.css('div.field-type-text-with-summary p::text').extract()[0].strip()

    	rows = response.css('div.view-project-basic-info div.view-content table tr td div.field-content').extract()
    	items = []
    	for row in rows:
    		sel = scrapy.Selector(text=row)
    		content = sel.xpath('.//div/text()').extract()
    		if not content:
    			content = sel.css('a::text').extract()
    			if not content:
    				content = sel.css('span::text').extract()
    				pass
    		pass
    		if(len(content) == 1):
    			items.append(content[0])
    		elif(len(content) > 1):
    			items.append(",".join(content))
    		else:
    			items.append("")
    	pass

    	project_id = items[0]

    	financeItems = []
    	financeRows =  response.css('div.view-project-finance-information table tr td div.field-content::text').extract()
    	total_cost = response.css('div.view-project-finance-information table tr td span.field-content::text').extract()[0]

    	for row in financeRows:
    		financeItems.append(row)
    	pass

    	documents = response.css('div.view-project-documents div.view-content ul li span.file a')
    	documentsList = []

    	for document in documents:
    		docDic = {}
    		docDic = {
    		'title': document.xpath('@title').extract_first(),
    		'link': document.xpath('@href').extract_first(),
    		'type': document.xpath('@type').extract_first(), 
    		'text' : document.css('::text').extract_first()
    		}

    		documentsList.append(docDic)
    		pass

    	dates = response.css('div.view-project-timeline div.timeline-box')
    	datesList = []

    	for date in dates:
    		dateItem = TimelineItem()
    		info = {}
    		info = {
    		'title': date.css('span.views-label::text').extract_first(), 
    		'date' : date.css('span.date-display-single::text').extract_first()
    		}

    		dateItem['project_id'] = project_id
    		dateItem['title'] = info.get('title')
    		dateItem['date'] = info.get('date')

    		datesList.append(info)

    		# yield(dateItem)
    		pass

    	
    	project_type = items[1]
    	status = items[2]
    	country = items[3]
    	region = items[4]
    	focal_areas = items[5]
    	funding_source = items[6]
    	implementing_agencies = items[7]
    	executing_agencies = items[8]
    	gef_period = items[9]
    	approval_fiscal_year = items[10]
    	project_preparation_grant_amount = financeItems[0]
    	gef_project_grant = financeItems[1]
    	co_financing_total = financeItems[2]
    	gef_agency_fees = financeItems[3]


    	item = GefItem()
    	

    	# for document in documentsList:
    	# 	documentItem = DocumentItem()

    	# 	documentItem['project_id'] = project_id
    	# 	documentItem['title'] = document.get("title")
    	# 	documentItem['type'] = document.get("type")
    	# 	documentItem['text'] = document.get("text")
    	# 	documentItem['link'] = document.get("link")

    	# 	yield(documentItem)
    	# 	pass

    	item['project_title'] = project_title
    	item['project_summary'] = project_summary
    	item['project_id'] = project_id
    	item['project_type'] = project_type
    	item['status'] = status
    	item['country'] = country
    	item['region'] = region
    	item['focal_areas'] = focal_areas
    	item['funding_source'] = funding_source
    	item['implementing_agencies'] = implementing_agencies
    	item['executing_agencies'] = executing_agencies
    	item['gef_period'] = gef_period
    	item['approval_fiscal_year'] = approval_fiscal_year
    	item['project_preparation_grant_amount'] = project_preparation_grant_amount
    	item['gef_project_grant'] = gef_project_grant
    	item['co_financing_total'] = co_financing_total
    	item['gef_agency_fees'] = gef_agency_fees
    	item['total_cost'] = total_cost
    	item['timeline'] = datesList
    	item['project_documents'] = documentsList

    	yield(item)