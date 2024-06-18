#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 13:42
# @Author  : Pointer
# @File    : mysql_engine.py
# @Software: PyCharm
from sqlalchemy import create_engine
from utils.config import config as db_config

# 使用 PyMySQL 驱动
def load_mysql_engine():
    # 设置连接池的大小和其他参数
    pool_args = {
        'pool_size': db_config["MYSQL"]["POOL_SIZE"],  # 连接池中的连接数
        'max_overflow': db_config["MYSQL"]["MAX_OVERFLOW"],  # 当连接池中的连接都被使用时，可以额外创建的最大连接数
        'pool_recycle': db_config["MYSQL"]["POOL_RECYCLE"],  # 多久之后自动回收连接（秒），设置为 None 则不回收
        'pool_pre_ping': db_config["MYSQL"]["POOL_PRE_PING"],  # 当从连接池中获取连接时，先检查连接是否有效
    }
    engine = create_engine(
        f'mysql+pymysql://{db_config["MYSQL"]["USERNAME"]}:{db_config["MYSQL"]["PASSWORD"]}'
        f'@{db_config["MYSQL"]["HOST"]}:{db_config["MYSQL"]["PORT"]}/{db_config["MYSQL"]["DBNAME"]}?charset=utf8mb4',
        pool_size=pool_args["pool_size"],max_overflow=pool_args["max_overflow"],pool_recycle=pool_args["pool_recycle"],pool_pre_ping=pool_args["pool_pre_ping"])
    return engine

# 或者，如果你使用的是 mysqlclient
# engine = create_engine('mysql://username:password@localhost/dbname')

# 其中：
# username: 你的 MySQL 用户名
# password: 你的 MySQL 密码
# localhost: MySQL 服务器地址（如果是本地数据库，则为 localhost）
# dbname: 你要连接的数据库名
