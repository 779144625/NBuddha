import logging
import os.path
import re
import json
import requests
import scrapy


class BuddhaSpider(scrapy.Spider):
    name = 'buddha'
    allowed_domains = ['weibo.com', 'sina.cn','weibocdn.com']
    start_urls = ['https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page=1&feature=0']

    origin_url = 'https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page='

    def parse(self, response):
        page_json = response.text  # 获取字符串
        list_img = json.loads(page_json)['data']['list'][1:]  # 解析list 第一个pass 没有实质性内容
        # print(list_img)
        for pic in list_img:
            # print(type(pic))
            retweeted_status = pic["retweeted_status"]  # 一般图片都在retweeted_status里面的pic_infos
            if "pic_infos" in retweeted_status:
                for key in retweeted_status["pic_infos"]:  # 无法判断是否有pic_infos 用try试一下
                    pic_infos = retweeted_status["pic_infos"][key]
                    # print(pic_infos)
                    url = pic_infos["mw2000"]["url"]  # 得到了高清图片的url
                    # print(url)
                    object_type = 'pic'
                    # yield scrapy.Request(
                    #     url=url,
                    #     callback=self.parse_obj,
                    #     meta={"type": object_type},
                    #     dont_filter=True  # 不要过滤相同的url
                    # )
            elif "page_info" in pic:
                print('0'*100)
                page_info = pic["page_info"]
                media_info = page_info["media_info"]
                url = media_info["stream_url_hd"]  # 获得了视频的url
                object_type = 'video'
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_obj,
                    meta={"type": object_type},
                    dont_filter=True  # 不要过滤相同的url
                )
            else:
                logging.DEBUG("Cant find page_info or pic_infos")
                exit(1)
        #     yield scrapy.Request(
        #         url=self.origin_url + f'{page}' + '&feature=0',
        #         callback=self.parse,
        #         meta={"item": item}
        #     )

    def parse_obj(self, response):
        """
            用于将目标保存到本地
        """
        path = './Download'
        url = response.request.url

        if not os.path.exists(path):
            os.mkdir(path)
        obj_type = response.meta["type"]
        if obj_type == "video":
            title = url.split('?')[0].split('/')[-1]
            # print('0'*100)
            try:
                with open(path + '/' + title, 'wb') as pic:
                    pic.write(response.body)
            except Exception as e:
                print(e)
                exit(1)
        elif obj_type == "pic":
            title = url.split('/')[-1]
            try:
                with open(path + '/' + title, 'wb') as pic:
                    pic.write(response.body)
            except Exception as e:
                print(e)
                exit(1)
        else:
            logging.DEBUG('Type is wrong')
            exit(1)
