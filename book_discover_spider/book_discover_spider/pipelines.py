# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class BookDiscoverMysqlPipeline:
    def process_item(self, item, spider):
        return item

class BookDiscoverMongoPipeline:
    def process_item(self, item, spider):
        return item

class BookDiscoverTestPipeline:
    def open_spider(self,spider):
        # self.f = open("./test.json","w",encoding="utf8")
        pass
    def process_item(self, item, spider):
        print(item)
        self.f = open(f"./static/{item['title']}.json", "w", encoding="utf8")
        self.f.write(json.dumps(item))
        self.f.close()
        return item

    def close_spider(self,spider):
        # self.f.close()
        pass