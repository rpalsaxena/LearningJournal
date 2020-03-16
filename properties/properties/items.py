# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PropertiesItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()


    ### Primary Fields
    title = Field()
    price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # Calculated fields
    images = Field()
    location = Field()

    ### HouseKeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
