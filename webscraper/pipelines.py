# -*- coding: utf-8 -*-

import os
import scrapy
from urllib import quote
from boto.aliyun.oss.connection import OSSConnection
from boto.aliyun.oss.key import Key
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

ALIYUN_ACCESS_KEY_ID = os.environ.get("ALIYUN_ACCESS_KEY_ID")
ALIYUN_SECRET_ACCESS_KEY = os.environ.get("ALIYUN_SECRET_ACCESS_KEY")
ALIYUN_STORAGE_BUCKET_NAME = os.environ.get("ALIYUN_STORAGE_BUCKET_NAME")
OSS_PREFIX = os.environ.get("OSS_PREFIX", "file_test")


class OSSUploadFilesPipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            req = scrapy.Request(file_url)
            req.meta["proxy"] = item["proxy"]
            req.meta["retry"] = 0
            yield req

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no files")
        ossConn = OSSConnection(
            aliyun_access_key_id=ALIYUN_ACCESS_KEY_ID,
            aliyun_secret_access_key=ALIYUN_SECRET_ACCESS_KEY,
        )
        b = ossConn.get_bucket(ALIYUN_STORAGE_BUCKET_NAME, validate=False)
        k = Key(b)
        k.key = OSS_PREFIX + '/' + item["filepath"]
        k.set_metadata("Content-Type", item["content_type"])
        k.set_metadata("Content-Disposition", "inline; filename*=utf-8''" +
                        quote(item["filename"], safe='!#$&+=.^_`|~'))
        size = k.set_contents_from_filename("file/"+file_paths[0])
        if size == 0:
            raise DropItem("the thumb upload error")
        item['file_paths'] = file_paths
        return item
