import os.path
import re

import requests
import scrapy


class BuddhaSpider(scrapy.Spider):
    name = 'buddha'
    allowed_domains = ['weibo.com', 'sina.cn']
    start_urls = ['https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page=1&feature=0']

    origin_url = 'https://weibo.com/ajax/statuses/mymblog?uid=2339808364&page='

    def parse(self, response):
        img_list = re.findall(
            '\"mw2000\":{\"url\":\"(.*?)\"', response.body.decode('gbk', 'ignore'))
        # print(response.body.decode('utf8','ignore'),'*'*100)
        page = 1  # 从第一页开始爬
        while True:
            if not img_list:  # 设置为终止条件
                break
            for img in img_list:  # 本页中所有图片
                # print('*'*100,'\n')
                item = {"img_url": img}
                # print(item)
                yield scrapy.Request(  # 发起详细请求，目标URL
                    url=item["img_url"],
                    callback=self.parse_img,
                    meta={"item": item},
                    dont_filter=True  # 不要过滤相同的url
                )
            page += 1
            yield scrapy.Request(
                url=self.origin_url + f'{page}' + '&feature=0',
                callback=self.parse,
                meta={"item": item}
            )

    def parse_img(self, response):
        """
            用于将图片保存到本地
        """
        path = './Download'
        if not os.path.exists(path):
            os.mkdir(path)
        item = response.meta["item"]
        img_url = item["img_url"]
        # print(img_url)
        title = img_url.split('/')[-1]
        image = requests.get(img_url, stream=True).content
        try:
            with open(path + '/' + title, 'wb') as jpg:
                jpg.write(image)
        except Exception as ex:
            print(ex)
        finally:
            jpg.close()
