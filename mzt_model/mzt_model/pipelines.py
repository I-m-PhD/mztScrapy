# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class MztModelPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request(
            url=item['photo_url'],
            meta={
                'model_name': item['model_name'],
                'album_title': item['album_title'],
            },
        )

    def file_path(self, request, response=None, info=None, *, item=None):
        fn = r'result-model/%s/%s/%s' % (request.meta['model_name'], request.meta['album_title'], request.url[-8:])
        return fn
