#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 17:41
# @Author  : Pointer
# @File    : mongo_engine.py
# @Software: PyCharm
from pymongo import MongoClient
from utils.config import config

def load_mongo_engine():
    mongo_config = config["MONGO"]
    client = MongoClient(mongo_config["CONNECTION_STRING"], maxPoolSize=mongo_config["MAXPOOLSIZE"], minPoolSize=mongo_config["MINPOOLSIZE"], waitQueueTimeoutMS=mongo_config["WAITQUEUETIMEOUTMS"])
    # 接下来，你可以像之前一样使用client来选择数据库和集合，并进行操作
    return client
    # db = client['mydatabase']
    # collection = db['mycollection']: