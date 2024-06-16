#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 1:31
# @Author  : Pointer
# @File    : md5.py
# @Software: PyCharm
import hashlib


def calculate_md5(input_string: str):
    # 创建一个md5 hash对象
    m = hashlib.md5()

    # 更新你想要哈希的数据
    m.update(input_string.encode('utf-8'))
    # 如果你想要一个可读的十六进制表示
    hex_digest = m.hexdigest()

    return hex_digest