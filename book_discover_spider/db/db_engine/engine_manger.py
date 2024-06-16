#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 16:13
# @Author  : Pointer
# @File    : engine_manger.py
# @Software: PyCharm

from db.db_engine.mysql_engine import load_mysql_engine
from db.db_engine.mongo_engine import load_mongo_engine
from utils import Singleton
class EngineManger(Singleton):

    def __init__(self):
        self.mysql_engine = load_mysql_engine()
        self.mongo_engine = load_mongo_engine()

    def get_mysql_engine(self):
        return self.mysql_engine

    def get_mongo_engine(self):
        return self.mongo_engine

    def get_engine(self,type):
        T = f"{type}_engine"
        if T not in self.__dict__:
            raise ValueError(f"{type} is not supported engine")
        return self.__getattribute__(f"get_{T}")()

engine_manger =  EngineManger()


if __name__ == '__main__':
    print(engine_manger.get_engine("mysql"))
    # print(engine_manger.get_engine("mongo"))