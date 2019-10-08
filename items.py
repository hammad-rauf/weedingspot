# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class WeddingspotItem(Item):

    images = Field()
    image_urls = Field()
    venue_title = Field()
    price = Field()
    style = Field()
    guest_capacity = Field()
    services = Field()
    location = Field()
    zip_code = Field()
    description = Field()
    venue_notes = Field()
    amenities = Field()
    restrictions = Field()
    url = Field()
    id = Field()
    web_url = Field()

    pass
