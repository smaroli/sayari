# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import *
import json
import pandas as pd
import csv

class NorthdakotascraperSpider(scrapy.Spider):
	name = 'northdakotascraper'
	allowed_domains = ['firststop.sos.nd.gov/search/business']
	start_urls = ['http://firststop.sos.nd.gov/search/business/']
	#initialize a global dataframe to be appended with extracted information
	global df
	df = pd.DataFrame(columns=['TITLE','RA','CRA','OWNER'])
	
	def start_requests(self):
		#submit post request to the request url based on search criteria (payload)
		url = 'https://firststop.sos.nd.gov/api/Records/businesssearch'
		headers = {'Content-type':'application/json', 'Accept':'*/*'}
		payload = {"SEARCH_VALUE": "X", "STARTS_WITH_YN": True, "ACTIVE_ONLY_YN": True}
		yield scrapy.FormRequest(url, callback=self.parse, method="POST",headers=headers,body=json.dumps(payload),dont_filter=True)

	def parse(self,response):
		final_list = []
		data = json.loads(response.body)
		#for each company submit a get request again based on the source_id of each company
		for each in data['rows'].keys():
			url1 = 'https://firststop.sos.nd.gov/api/FilingDetail/business/'+each+'/false'
			headers1 = {'Content-type':'application/json', 'Accept':'*/*'}
			yield scrapy.FormRequest(url1,callback=self.parse_results,method="GET",headers=headers1,body=None,dont_filter = True,meta={'name':each,'title':data['rows'][each]['TITLE'][0]})
		  
	def parse_results(self,response):
		data = json.loads(response.body)
		name = response.meta['name']
		#extract company, registered agent and commercial registered agent for each company
		for each in data['DRAWER_DETAIL_LIST']:
			df.loc[name,'TITLE'] = response.meta['title']
			if each['LABEL'] == 'Owner Name':
				df.loc[name,'OWNER'] = each['VALUE']
			if each['LABEL'] == 'Commercial Registered Agent':
				df.loc[name,'CRA'] = each['VALUE']
			if each['LABEL'] == 'Registered Agent':
				df.loc[name,'RA'] = each['VALUE']
			df.to_csv('northdakotaexport.csv')