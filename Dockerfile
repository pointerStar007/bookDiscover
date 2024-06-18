FROM centos:7.8.2003

RUN curl -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.tuna.tsinghua.edu.cn/centos/7/os/x86_64/repodata/repomd.xml.asc
RUN yum clean all && yum makecache
RUN yum install -y gcc
RUN curl https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh -o Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh && bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH /opt/conda/bin:$PATH
RUN /opt/conda/bin/conda create -y -n biquge python=3.10.14
RUN conda init bash && source ~/.bashrc && conda activate biquge && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip install scrapy==2.8.0 scrapy-redis==0.7.3 twisted==22.2.0 pymysql==1.1.1 pymongo==4.7.3 SQLAlchemy==2.0.30 PyYAML==6.0.1
# 将当前目录下的 book_discover_spider 目录复制到容器的 /book_discover_spider 目录下
COPY ./book_discover_spider /book_discover_spider
# 设置工作目录为 /book_discover_spider
WORKDIR /book_discover_spider
#RUN #echo "conda init bash && source ~/.bashrc && conda activate biquge && scrapy crawl biquge" > /start.sh
#RUN #chmod +x /start.sh
ENV PYTHONPATH=/book_discover_spider

# 设置容器启动时运行的命令
#CMD ["sh","/start.sh"]
CMD ["/opt/conda/envs/biquge/bin/scrapy","runspider","/book_discover_spider/book_discover_spider/spiders/biquge.py"]
# 初始化mysql ["/opt/conda/envs/biquge/bin/python","/book_discover_spider/db/model/mysql_model.py"]