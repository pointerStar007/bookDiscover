#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 13:46
# @Author  : Pointer
# @File    : config.py
# @Software: PyCharm
import sys
import yaml
from utils import Singleton
from collections import UserDict
class Config(Singleton,UserDict):

    def __init__(self):
        super(Config, self).__init__()
        self.load_config()

    def load_config(self):
        with open('/book_discover_spider/conf/config.yaml', 'r', encoding="utf8") as file:
            self.data = yaml.safe_load(file)

config = Config()

if __name__ == '__main__':
    print(config)