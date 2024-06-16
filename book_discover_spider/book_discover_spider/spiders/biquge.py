from scrapy_redis.spiders import RedisSpider
from scrapy import Spider, Request
import time
import re
from utils import calculate_md5,config
import os


class BiqugeSpider(RedisSpider):
    name = "biquge"
    # allowed_domains = ["bbiquge.la"]
    redis_key = 'book_discover:start_urls'
    # start_urls = ['https://www.bbiquge.la/book_1/']

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(','))) if domain else ["bbiquge.la"]
        super(BiqugeSpider, self).__init__(*args, **kwargs)

    def parse(self, response):

        if len(response.xpath("//div[@class='blockcontent']/div/text()")) != 0 and "文章不存在" in response.xpath("//div[@class='blockcontent']/div/text()").extract_first():
            return # 没有更多书籍了

        img_url = response.xpath(r"//div[@id='fmimg']/img/@src").extract_first()  # 封面
        is_finish = True if response.xpath(
            r"//div[@id='fmimg']/span/@class").extract_first() == "red" else False  # 是否完结
        book_type = response.xpath("//div[@class='con_top']/text()").extract_first().split(">")[1]  # 书类别
        info = response.xpath("//div[@id='info']")  # 信息节点
        book_name = info.xpath('./h1/text()').extract_first()  # 书名
        book_author = info.xpath('./p[1]/a/text()').extract_first()  # 作者
        update_time, word_count = info.xpath('./p[3]/text()').extract_first().replace("\xa0", "$").split("$")
        update_time = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", update_time)[0] if len(
            update_time) > 0 else ""  # 更新时间
        word_count = re.findall(r'\d+万字', word_count)[0] if len(word_count) > 0 else ""  # 字数
        last_chapter = info.xpath("./p[4]/a/text()").extract_first()  # 最新内容标题
        info_text = "".join(info.xpath(r".//div[@id='intro']/text()").extract_first().split())  # 简介

        c_list = response.xpath(r"//dl//dd/a")  # 章节列表
        chapter_list = []
        for title, href in zip(c_list.xpath("./text()").extract(), c_list.xpath("./@href").extract()):
            chapter = {"title": title, "href": href}
            if chapter in chapter_list:
                chapter_list.remove(chapter)  # 去除前边重复的章节
            chapter_list.append(chapter)

        for index, item in enumerate(chapter_list): # 章节列表
            item["index"] = index

        book = {
            "_id": calculate_md5(book_name+book_author),
            "book_name": book_name,
            "info": info_text,
            "author": book_author,
            "cover_path": calculate_md5(img_url)+".png",
            "book_type": book_type,
            "word_count": word_count,
            "chapter_total": len(chapter_list),
            "is_finish": is_finish,
            "last_chapter": last_chapter,
            "last_update_time": update_time,
            "chapters": [{"id": calculate_md5(item["title"] + item["href"]),
                          "chapterindex": item["index"], "text": item["title"]} for item in chapter_list]
        }
        for item in chapter_list: # 获取详情页
            yield Request(url=response.request.url + item["href"], meta={"book": book,"chapterindex":item["index"],"_id": calculate_md5(item["title"] + item["href"])},callback=self.praseContent) # 请求详情页数据

        url = f'https://www.bbiquge.la/book/{int(response.request.url.split("_")[1][:-1])+1}'
        yield Request(url=url,callback=self.parse,dont_filter=True) # 不去重方便增量更新
        yield Request(url=img_url,callback=self.img_save)

    def praseContent(self, response):
        content = response.xpath("//div[@id='content']/text()").extract() # 取正文
        content = "<br><br>".join(content[1:-1]).replace("\xa0", "&nbsp;") # 格式化正文
        title = response.xpath("//h1/text()").extract_first() # 取标题
        _id = response.meta.get("_id")
        chapterindex = response.meta.get("chapterindex")
        book = response.meta.get("book")
        books_content_ = {
            "_id": _id,
            "title":title,
            "chapterindex":chapterindex,
            "content":content,
            "book_id": book["_id"],
            "book_name":book["book_name"],
            "book_author":book["author"],
            "book_type":book["book_type"],
            "book":book
        }
        yield books_content_


    def img_save(self,response):
        with open(os.path.join(config["STATIC_DIR"],calculate_md5(response.request.url)+".png"),"wb") as f:
            f.write(response.content)