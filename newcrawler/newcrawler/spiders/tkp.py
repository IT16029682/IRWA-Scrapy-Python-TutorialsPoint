# -*- coding: utf-8 -*-
import scrapy
from ..items import CodeItem

class TkpSpider(scrapy.Spider):
    name = 'tkp'
    allowed_domains = ['www.tutorialspoint.com']
    start_urls = ['https://www.tutorialspoint.com/java/java_basic_syntax.htm']

    def parse(self, response):
        #tk=response.css('.prettyprint')
        #dess=response.css('p::text').extract()
        title=response.xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div/h1/text()').extract_first()

        subtitles=response.xpath('//h2[not(contains(.,"What is Next?"))]/text()').extract()
        count = 1
        #titlelist=dict()
        for t in subtitles:
            #code = t.css('.prettyprint::text').extract_first()
            description = response.xpath('//p[count(preceding-sibling::h2)=' + str(count) + ']/text()').extract()
            code=response.xpath('//pre[count(preceding-sibling::h2)='+ str(count) +' ]/text()').extract()  
            language=title.split()[0]
            #print(code)
            Item=CodeItem()
            Item['Title']=title[7:] + ' - ' + t
            Item['Code']=code
            #Item['Subtitle']=t
            Item['Language']=language
            Item['Description']=description
            Item['URL']= response.request.url
            count+=1
            yield Item
        
        NextLinkSelector= response.xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div/div[4]/a/@href')
        if NextLinkSelector:
           NextLink=NextLinkSelector.extract_first()
           yield scrapy.Request(url=response.urljoin(NextLink))    

