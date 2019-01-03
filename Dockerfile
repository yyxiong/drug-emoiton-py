FROM python:3.7.2
ENV PATH /usr/local/bin:$PATH
ADD . /drug-emotion
WORKDIR /drug-emotion
RUN pip3 install -r requirements.txt
CMD cd spiders && scrapy crawl net39
