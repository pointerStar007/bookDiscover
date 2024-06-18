#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 18:52
# @Author  : Pointer
# @File    : mongo_crud.py
# @Software: PyCharm


from db.db_engine import engine_manger
from datetime import datetime

client = engine_manger.get_mongo_engine()


class MongoCRUDBook:
    coll = client["books"]["books"]

    # 插入一本新书
    @classmethod
    def insertBook(cls, book):
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        book["update_time"] = now_time
        book["is_delete"] = False
        try:
            # cls.coll.insert_one(book)
            cls.coll.update_one(
            {"_id":book["_id"]},
            { "$set": book,
              "$setOnInsert": {"create_time": now_time}  # 仅在新建文档时设置
               },
            upsert=True
            ) # 增量更新章节部分
        except:
            return
    @classmethod
    def queryBookByID(cls, id: str):
        return cls.coll.find_one({"_id": id})

    @classmethod
    def queryBooksByBooksName(cls, book_name: str):
        return list(cls.coll.find({"book_name": book_name}))

    @classmethod
    def queryBooksByAuthor(cls, author: str):
        return list(cls.coll.find({"author": author}))

    @classmethod
    def queryBooksByISFinish(cls, is_finish: bool):
        return list(cls.coll.find({"is_finish": is_finish}))


# 插入一个章节
class MongoCRUDChapter:
    db = client["books_content"]

    @classmethod
    def insertChapter(cls, content):
        try:
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content["create_time"] = now_time
            content["is_delete"] = False
            cls.db[content["book_id"]].insert_one(content)
        except:
            return

    @classmethod
    def queryChapterByID(cls, book_id, id):
        return cls.db[book_id].find_one({"_id": id})

class MongoCRUDBookShelf:
    pass # TODO 书架

class MongoCRUDSubscribes:
    pass # TODO 订阅

class MongoCRUDReadLog:
    pass # TODO 阅读记录





if __name__ == '__main__':
    pass
    # print(queryBooksByBooksName("完美世界"))
