# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

logger = logging.getLogger(__name__)
# useful for handling different item types with a single interface
class NbuddhaPipeline:
    def process_item(self, item, spider):
        logger.warning(item)
        path = './Download'
        url = item['url']
        body = item['body']
        if not os.path.exists(path):
            os.mkdir(path)
        obj_type = item['type']
        if obj_type == "video":
            title = url.split('?')[0].split('/')[-1]
            try:
                with open(path + '/' + title, 'wb') as pic:
                    pic.write(body)
            except Exception as e:
                logging.debug(e)
                exit(1)
        elif obj_type == "pic":
            title = url.split('/')[-1]
            try:
                with open(path + '/' + title, 'wb') as pic:
                    pic.write(body)
            except Exception as e:
                logging.debug(e)
                exit(1)
        else:
            logging.debug('Type is wrong')
            exit(1)
        return item  # 必须return item以供别的pipeline使用
