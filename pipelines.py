import scrapy
from scrapy.pipelines.images import ImagesPipeline


class WeddingspotPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):       

        count = 0
        for img_url in item['image_urls']:
            count += 1
            yield scrapy.Request(img_url, meta={'image_name': item["id"],'count': count})

    def file_path(self, request, response=None, info=None):

        return f"{request.meta['image_name']}-{request.meta['count']}.jpg" 
