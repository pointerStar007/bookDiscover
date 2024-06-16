#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 13:48
# @Author  : Pointer
# @File    : Singleton.py
# @Software: PyCharm


# 单例

class Singleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

class A(Singleton):
    pass
if __name__ == '__main__':
    a1 = A()
    a2 = A()
    print(id(a1))
    print(id(a2))