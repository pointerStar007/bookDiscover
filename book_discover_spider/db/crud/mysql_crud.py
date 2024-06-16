#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 16:53
# @Author  : Pointer
# @File    : mysql_crud.py
# @Software: PyCharm

from db.model.mysql_model import *  # 导入所有模型
from db.db_engine import engine_manger
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_, between

Session = sessionmaker(bind=engine_manger.get_mysql_engine())


# Author
def queryAuthorByName(name: str) -> Author:
    session = Session()
    author = session.query(Author).filter(Author.name == name).first()
    return author


def inertAuthor(name: str):
    session = Session()
    author = Author()
    author.name = name
    session.add(author)
    session.commit()

# BookType
def queryBookTypeByName(name:str)->BookType:
    session = Session()
    bookType = session.query(BookType).filter(BookType.name == name).first()
    return bookType

def inertBookType(name:str):
    session = Session()
    bookType = BookType()
    bookType.name = name
    session.add(bookType)
    session.commit()

if __name__ == '__main__':
    print(queryAuthorByName("辰东"))
