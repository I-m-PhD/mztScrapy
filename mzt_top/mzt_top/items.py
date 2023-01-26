# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MztTopItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model_name = scrapy.Field()
    album_head = scrapy.Field()
    img_url = scrapy.Field()
