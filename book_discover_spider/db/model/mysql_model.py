#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/16 14:53
# @Author  : Pointer
# @File    : mysql_model.py
# @Software: PyCharm


from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean,BigInteger,Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from utils import ReprMixin
from enum import Enum as REnum

Base = declarative_base()


class Perission(REnum):
    READONLY = "ReadOnly"
    READANWRITE = "ReadandWrite"
    SUPER = "super"


class Status(REnum):
    NORMAL = "normal"
    ABNORMAL = "abnormal"

class OperateType(REnum):
    QUERY = "query"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"


class Account(Base, ReprMixin):
    __tablename__ = 'table_account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), unique=True, nullable=False)  # 用户名
    label = Column(String(30), nullable=False, default="未命名-代号")  # 代号
    password = Column(String(255), nullable=False)  # 密码
    salt = Column(String(255),default="book_discover",nullable=False) # 密码盐值
    email = Column(String(255), nullable=False)  # 邮箱，支持邮箱找回，邮箱验证登录，变更通知, 登陆提醒
    last_login_time = Column(DateTime, default="1970-1-1 0:0:0")  # 最后一次上线时间
    last_login_ip = Column(String(16), nullable=False, default="0.0.0.0") # 最后一次上线的 ip 地址
    permissions = Column(Enum(Perission), default=Perission.READANWRITE, nullable=False) # 权限
    status = Column(Enum(Status), default=Status.NORMAL, nullable=False) # 账号状态
    is_delete = Column(Boolean, nullable=False, default=False) # 逻辑删除
    create_time = Column(DateTime, server_default=func.now(), nullable=False) # 创建时间

class User(Base,ReprMixin):
    __tablename__ = "table_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)  # 邮箱，邮箱验证登录，订阅更新提醒
    name = Column(String(30), nullable=False,default="道友请斩14境大妖")  # 昵称
    avatar = Column(String(255),nullable=False,default="default.png") # 头像
    status = Column(Enum(Status),nullable=False,default=Status.NORMAL) # 账号状态
    create_time = Column(DateTime, server_default=func.now(), nullable=False) # 创建时间


class VisitLog(Base,ReprMixin):
    __tablename__ = "table_user_visits_log" # 用户访问记录
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    ip_addr = Column(String(16), nullable=False, default="0.0.0.0") # 用户 ip 地址
    email = Column(String(255), nullable=True,default="")  # 邮箱 是否登录
    visit_log = Column(Text, nullable=False) # 访问记录
    """
        ip_addr: ip地址
        url： 访问的路由
        paramss: 访问的参数信息
        time: 访问的时间
    """
    status = Column(Enum(Status), nullable=False, default=Status.NORMAL)  # 访问状态，异常会立即拉黑 ip 地址
    create_time = Column(DateTime, server_default=func.now(), nullable=False) # 创建时间
    is_delete = Column(Boolean, nullable=False, default=False) # 逻辑删除

class Operate(Base,ReprMixin):
    __tablename__ = "table_operate" # 管理日志
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    operate = Column(String(255),nullable=False) # 操作 接口
    params = Column(String(255),nullable=False,default="") # 接口参数
    type = Column(Enum(OperateType),nullable=False,default=OperateType.QUERY)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    is_delete = Column(Boolean, nullable=False, default=False)  # 逻辑删除


class Author(Base,ReprMixin):
    __tablename__ = "table_author" # 作者表
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, default="")  # 作者昵称
    create_time = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    update_time = Column(DateTime, server_default=func.now(), nullable=False)  # 变更时间
    is_delete = Column(Boolean, nullable=False, default=False)  # 逻辑删除


class BookType(Base, ReprMixin):
    __tablename__ = "table_book_type"  # 小说类别信息
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False, default="")  # 类别
    create_time = Column(DateTime, server_default=func.now(), nullable=False)  # 创建时间
    update_time = Column(DateTime, server_default=func.now(), nullable=False)  # 变更时间
    is_delete = Column(Boolean, nullable=False, default=False)  # 逻辑删除


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from utils.config import config as db_config
    engine = create_engine(f'mysql+pymysql://{db_config["MYSQL"]["USERNAME"]}:{db_config["MYSQL"]["PASSWORD"]}'
        f'@{db_config["MYSQL"]["HOST"]}:{db_config["MYSQL"]["PORT"]}/{db_config["MYSQL"]["DBNAME"]}?')
    Base.metadata.create_all(engine)