#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/15 21:38
# @Author  : Pointer
# @File    : readme.py
# @Software: PyCharm


#  book_discover_spider 项目的爬虫模块

#  依赖于 scrapy-redis 搭建分布式爬虫

#  采用当今最流行的 容器化部署方案 k8s 在 4个 节点上组建集群，1个 master 节点，3个 node 节点

# python version： 3.10.14

# requirements.txt  相关依赖文件

#  最终会打包成为一个 image 直接 push 到仓库，然后部署在 k8s 集群，即会自动开始分布式扫描全站，进行增量抓取内容
