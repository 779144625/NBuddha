import json
import logging

import scrapy


class BuddhaSpider(scrapy.Spider):
    name = 'buddha'
    allowed_domains = ['weibo.com', 'sina.cn', 'weibocdn.com']

    start_urls = ['https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page=1&feature=0']
    origin_url = 'https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page='

    def parse(self, response):
        page_json = response.text  # 获取字符串
        list_img = json.loads(page_json)['data']['list'][1:]  # 解析list 第一个pass 没有实质性内容
        # print(list_img)
        for l in list_img:
            # print(type(pic))
            retweeted_status = l["retweeted_status"]  # 一般图片都在retweeted_status里面的pic_infos
            if "pic_infos" in retweeted_status:
                for key in retweeted_status["pic_infos"]:  # 无法判断是否有pic_infos 用try试一下
                    pic_infos = retweeted_status["pic_infos"][key]
                    # print(pic_infos)
                    url = pic_infos["mw2000"]["url"]  # 得到了高清图片的url
                    # print(url)
                    object_type = 'pic'
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse_obj,
                        meta={"type": object_type},
                        dont_filter=True  # 不要过滤相同的url
                    )
            elif "page_info" in l:
                # print('0'*100)
                page_info = l["page_info"]
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
                # 考虑到C哥的社会属性，有时候会转发一些文字内容，不包含图片和gif的，所以如果找不到这两个属性在当前这一part，就切换到下一个属性好了
                logging.warning("Cant find page_info or pic_infos")
                continue
        page = int(response.request.url.split('=')[2][0]) + 1
        print(page)
        yield scrapy.Request(
            url=self.origin_url + f'{page}' + '&feature=0',
            callback=self.parse,
            meta={}
        )

    def parse_obj(self, response):
        """
            传递给pipelines进行下载保存
        """
        url = response.request.url
        item = {
            'url': url,
            'type': response.meta['type'],
            'body': response.body
        }
        yield item
