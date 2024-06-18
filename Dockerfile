FROM python:3.10.14-alpine

RUN pip install scrapy==2.8.0 scrapy-redis==0.7.3 twisted==22.2.0 pymysql==1.1.1 pymongo==4.7.3 SQLAlchemy==2.0.30  PyYAML==6.0.1

COPY ./book_discover_spider /book_discover_spider
WORKDIR /book_discover_spider
ENV PYTHONPATH=/book_discover_spider

CMD ["scrapy", "runspider", "/book_discover_spider/book_discover_spider/spiders/biquge.py"]

# 最优解