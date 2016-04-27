import os
import scrapy
import json
import random
from datetime import datetime
from urlparse import urlparse
from scrapy.utils.project import get_project_settings
from webscraper.items import FileItem

class InstagramSpider(scrapy.Spider):
    name = "instagram"
    allowed_domains = get_project_settings().get("ALLOWED_DOMAINS")
    source_type = get_project_settings().get("SOURCE_TYPE")

    def __init__(self, *args, **kwargs):
        super(InstagramSpider, self).__init__(*args, **kwargs)
        settings = get_project_settings()
        self.source_type = settings.get("SOURCE_TYPE")
        self.users = []

        for line in open(settings.get("USER_LIST")):
            line = line.strip('\n')
            self.users.append(line)

    def start_requests(self):
        requests = []
        print(self.users)
        for username in self.users:
            req = scrapy.Request("https://www.instagram.com/%s/" % username,
                             callback=self.instagram_parse)
            req.meta['proxy'] = True
            yield req

    def instagram_parse(self, response):
        res = response.xpath('//script/text()').re(r'window._sharedData = \s*(.*);$')[0].encode("utf-8")
        data = json.loads(res)
        u = data["entry_data"]["ProfilePage"][0]["user"]
        for n in u["media"]["nodes"]:
            title = ""
            if "caption" in n:
                title = n["caption"]
            mediaType = "image"
            filename = datetime.now().strftime('%y%m%d%H%M%S') + str(random.randint(0, 1000))
            thumb = "%s/img/%s" % (1, filename)
            storage = ""
            if n["is_video"]:
                storage = "%s/vod/%s" % (1, filename)
                mediaType = "vod"
                url = "https://www.instagram.com/p/%s/?taken-by=%s&__a=1" % (n["code"], u["username"])
                req = scrapy.Request(url, callback=self.get_instagram_video)
                req.meta["filename"] = filename+".mp4"
                req.meta["proxy"] = True
                req.meta["storage"] = storage
                yield req
            item = FileItem()
            item["file_urls"] = [n["display_src"]]
            item["filepath"] = thumb
            item["filename"] = filename+".jpg"
            item["content_type"] = "image/jpeg"
            item["proxy"] = True
            yield item

    def get_instagram_video(self, response):
        data = json.loads(response.body)
        item = FileItem()
        item["file_urls"] = [data["media"]["video_url"]]
        item["filepath"] = response.meta["storage"]
        item["filename"] = response.meta["filename"]
        item["content_type"] = "video/mpeg4"
        item["proxy"] = True
        yield item
