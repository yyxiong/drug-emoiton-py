# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from net39.items import DrugItem, DrugComment

class DuplicatesPipeline(object):
  '''
  重复数据处理
  '''
  def __init__(self):
    self.drugs_seen = set()
    self.comments_seen = set()

  def process_item(self, item, spider):
    '''
    过滤重复数据
    '''
    if isinstance(item, DrugItem):
      if item['name'] is None:
        pass
      else:
        drug_id = item['drug_id']
        if drug_id in self.drugs_seen:
          pass
        else:
          self.drugs_seen.add(drug_id)
          return item
    elif isinstance(item, DrugComment):
      comment_id = item['comment_id']
      if comment_id in self.comments_seen:
        pass
      else:
        self.comments_seen.add(comment_id)
        return item
    else:
      return item

class DrugPipeline(object):
  def __init__(self, mongo_uri, mongo_db):
    self.mongo_uri = mongo_uri
    self.mongo_db = mongo_db

  @classmethod
  def from_crawler(cls, crawler):
    return cls(
      mongo_uri=crawler.settings.get('MONGO_URI'),
      mongo_db=crawler.settings.get('MONGO_DATABASE')
    )

  def open_spider(self, spider):
    self.client = pymongo.MongoClient(self.mongo_uri)
    self.db = self.client[self.mongo_db]
    # self.db['drug'].create_index([('drug_id')], unique=True)
    # self.db['comment'].create_index([('comment_id')], unique=True)

  def close_spider(self, spider):
    self.client.close()

  def process_item(self, item, spider):
    if isinstance(item, DrugItem):
      self.db['drug'].update({'drug_id': item['drug_id']}, dict(item), upsert=True)
      return item
    elif isinstance(item, DrugComment):
      self.db['comment'].update({'comment_id': item['comment_id']}, dict(item), upsert=True)
      return item
    else:
    #   print(item)
      return