# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

from itemadapter import ItemAdapter
import json
from db.crud import mysql_crud,mongo_crud


class BookDiscoverMysqlPipeline:
    """
    books_content_ = {
            "_id": _id,
            "title":title,
            "chapterindex":chapterindex,
            "content":content,
            "book":book
        }
    book = {
            "book_name": book_name,
            "info": info_text,
            "author": book_author,
            "cover_path": img_url,
            "book_type": book_type,
            "word_count": word_count,
            "chapter_total": len(chapter_list),
            "is_finish": is_finish,
            "last_chapter": last_chapter,
            "last_update_time": update_time,
            "chapters": [{"id": calculate_md5(item["title"] + item["href"]),
                          "chapterindex": item["index"], "text": item["title"]} for item in chapter_list]
        }

    """
    def process_item(self, item, spider):
        # 检查 作者信息是否又被记录，没有则添加
        author = mysql_crud.queryAuthorByName(item["book"]["author"])
        if not author:
            mysql_crud.inertAuthor(item["book"]["author"])
            author = mysql_crud.queryAuthorByName(item["book"]["author"])
        item["book"]["author_id"] = author.id
        item["book_author_id"] = author.id
        # 检查 书分类信息是否被记录，没有则添加
        book_type = mysql_crud.queryBookTypeByName(item["book"]["book_type"])
        if not book_type:
            mysql_crud.inertBookType(item["book"]["book_type"])
            book_type = mysql_crud.queryBookTypeByName(item["book"]["book_type"])
        item["book"]["book_type_id"] = book_type.id
        item["book_type_id"] = book_type.id

        logging.debug(item)

        return item

class BookDiscoverMongoPipeline:
    def process_item(self, item, spider):
        mongo_crud.MongoCRUDBook.insertBook(item["book"])
        del item["book"]
        mongo_crud.MongoCRUDChapter.insertChapter(item)
        return item

# class BookDiscoverTestPipeline:
#     def open_spider(self,spider):
#         # self.f = open("./test.json","w",encoding="utf8")
#         pass
#     def process_item(self, item, spider):
#         print(item)
#         self.f = open(f"./static/{item['title']}.json", "w", encoding="utf8")
#         self.f.write(json.dumps(item))
#         self.f.close()
#         return item
#
#     def close_spider(self,spider):
#         # self.f.close()
#         pass