# -*- coding: utf-8 -*-
import scrapy
from properties.items import PropertiesItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from urllib.parse import urljoin

class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['localhost:9312']
    start_urls = ['http://localhost:9312/properties/property_000000.html']

    def parse(self, response):
        l = ItemLoader(item=PropertiesItem(), response=response)
        l.add_xpath('title',
                    '//*[@itemprop="name"][1]/text()',
                    MapCompose(str.strip, str.title))

        l.add_xpath('price', '//*[@itemprop="price"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''), float),
                    re= '[,.0-9]+'
                    )

        l.add_xpath('description',
                    '//*[@itemprop="description"][1]/text()',
                    MapCompose(str.strip), Join())

        l.add_xpath('address',
                    '//*[@itemtype="http://schema.org/Place"]/text()',
                    MapCompose(str.strip))

        l.add_xpath('image_urls',
                    '//*[@itemprop="image"][1]/@src',
                    MapCompose(lambda i: urljoin(response.url, i)))

        return l.load_item()
