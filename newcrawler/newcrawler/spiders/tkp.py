# -*- coding: utf-8 -*-
import scrapy
from ..items import CodeItem

class TkpSpider(scrapy.Spider):
    name = 'tkp'
    allowed_domains = ['www.tutorialspoint.com']
    start_urls = ['https://www.tutorialspoint.com/java/java_basic_syntax.htm']

    def parse(self, response):
        tk=response.css('.prettyprint')
        dess=response.css('p::text').extract()
        #titlelist=dict()
        for t in tk:
            code = t.css('.prettyprint::text').extract_first()
            title=t.xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div/h1/text()').extract_first()
            language=title.split()[0]
            #print(code)
            Item=CodeItem()
            Item['Title']=title[7:]
            Item['Code']=code
            Item['Language']=language
            Item['Description']=dess
            Item['URL']= response.request.url
            yield Item
        
        NextLinkSelector= response.xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div/div[4]/a/@href')
        if NextLinkSelector:
           NextLink=NextLinkSelector.extract_first()
           yield scrapy.Request(url=response.urljoin(NextLink))    

