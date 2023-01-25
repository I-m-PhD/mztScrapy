# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MztModelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model_name = scrapy.Field()
    album_title = scrapy.Field()
    photo_url = scrapy.Field()
