from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import WeddingspotItem

import logging

import js2xml
import lxml.etree
from parsel import Selector

import re
import json

class WeddingspotSpider(CrawlSpider):

    name = 'weddingspot'
    start_urls = [
        'https://www.wedding-spot.com/'
    ]
    
    id = 200000
    
    rules = (
        Rule(LinkExtractor(restrict_css = '#see-more')),
        Rule(LinkExtractor(restrict_css = ".locations-list a[href^='/cities']")),
        Rule(LinkExtractor(restrict_css = [".cities-list .text-center a",'#pagination-next-btn'])),
        Rule(LinkExtractor(restrict_css = "#list-view .venue-box-wrapper"), callback = 'parsee'),
    )

    def parsee(self, response):

        item = WeddingspotItem()

        item['id'] = self.id
        self.id = self.id + 1

        item['image_urls'] = response.css('.slick-slide img::attr(src)').extract()

        item['venue_title'] = response.css('.Panel--className .SecondaryCTA--venueName::text').extract_first()
        item['venue_title'] = item['venue_title'].replace("'","")

        price = response.css('.Panel--className .VenuePrimaryCTA--className h3::text').extract()
        a = ' '       
        item['price'] =  a.join(price)
        item['price'] = item['price'].replace("'","")

        item['style'] = response.css('.VenuePage--main-details .VenuePage--detail-text-container p::text').extract_first()
        item['style'] = item['style'].replace("'","")

        item['guest_capacity'] = response.css('.VenuePage--main-details .VenuePage--detail-text-container p::text').extract()[1]
        item['guest_capacity'] = item['guest_capacity'].replace("'","")

        services = response.css('.VenuePage--main-details .VenuePage--detail-text-container p::text').extract()[2:4]
        b = ','       
        item['services'] =  b.join(services)
        item['services'] = item['services'].replace("'","")

        item['location'] = response.css('.VenuePage--main-details .VenuePage--detail-text-container p::text').extract()[4]
        item['location'] = item['location'].replace("'","")

        item['zip_code'] = response.css('.VenuePage--main-details .VenuePage--detail-text-container span::text').extract_first()
        item['zip_code'] = item['zip_code'].replace("'","")

        item['description'] = response.css('.VenuePage--description p::text').extract_first()
        item['description'] = item['description'].replace("'","")

        item['venue_notes'] = response.css('p.VenuePage--additional-detail::text').extract_first()
        item['venue_notes'] = item['venue_notes'].replace("'","")

        item['url'] = response.url

        amenities = response.css('.Amenities--row .VenuePage--additional-detail')[0]
        amenities = amenities.css('.VenuePage--additional-detail p::text').extract()
        amenities = [value for value in amenities if value != '- ']
        c = ','       
        item['amenities'] =  c.join(amenities)
        item['amenities'] = item['amenities'].replace("'","")

        restrictions = response.css('.Amenities--row .VenuePage--additional-detail')[1]
        restrictions = restrictions.css('.VenuePage--additional-detail p::text').extract()
        restrictions = [value for value in restrictions if value != '- ']
        d = ','       
        item['restrictions'] =  d.join(restrictions)
        item['restrictions'] = item['restrictions'].replace("'","")

        javascript = response.css("script:contains('window.__PRELOADED_STATE__')::text").get() 
        xml = lxml.etree.tostring(js2xml.parse(javascript), encoding='unicode')
        selector = Selector(xml)
        junk  = javascript[javascript.index('website'):]
        http = junk[junk.index('http'):]
        http = http[:http.index('"')]
        item['web_url'] = http         


        f = open("data.txt", "a")
        f.write(f"({item['id']},'{item['venue_title']}','{item['price']}','{item['style']}','{item['guest_capacity']}','{item['services']}','{item['location']}','{item['zip_code']}','{item['description']}','{item['venue_notes']}','{item['url']}','{item['amenities']}','{item['restrictions']}','{item['web_url']}'),\n")
        f.close()

        yield item
