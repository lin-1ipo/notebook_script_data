# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    title = scrapy.Field()
    body = scrapy.Field()


class Restaurant(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    station = scrapy.Field()
    score = scrapy.Field()


class Review(scrapy.Item):
    name = scrapy.Field()
    score = scrapy.Field()
    text = scrapy.Field()
