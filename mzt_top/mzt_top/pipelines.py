# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MztTopPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(
            url=item['img_url'],
            meta={
                'model_name': item['model_name'],
                'album_head': item['album_head'],
            },
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        fn = r'top/%s/%s/%s' % (request.meta['model_name'], request.meta['album_head'], request.url[-8:])
        return fn
