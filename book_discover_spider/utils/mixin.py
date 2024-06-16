#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 14:55
# @Author  : Pointer
# @File    : mixin.py
# @Software: PyCharm


class ReprMixin:

    def __repr__(self):
        # 获取类名
        class_name = self.__class__.__name__

        # 获取所有属性及其值，并格式化为字符串
        attrs = ', '.join(f'{key}={value!r}' for key, value in self.__dict__.items() if not key.startswith("_"))

        # 返回完整的字符串表示
        return f'{class_name}({attrs})'

# class A(ReprMixin):
#     def __init__(self,a,b,c):
#         self.a = a
#         self.b = b
#         self.c = c

if __name__ == '__main__':
    pass
    # a = A(1, 2, 3)
    # print(a)
