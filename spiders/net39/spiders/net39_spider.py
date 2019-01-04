import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from net39.items import DrugItem, DrugComment
from net39.spiders.net39_parser import parse_drug_item, parse_drug_comments

class Net39Spider(CrawlSpider):
  name = 'net39'
  allowed_domains = ['ypk.39.net']
  start_urls = ['http://ypk.39.net/']
  # start_urls = ['http://ypk.39.net/569620/']
  # start_urls = ['http://ypk.39.net/508685/comment']

  item_pattern = r'/\d+/$'
  comment_pattern = r'/\d+/comment$'

  rules = [
    Rule(
      LinkExtractor(
        deny=('search/*', '.html', '.aspx', item_pattern)
      ),
      callback='parse_list'
    ),
    Rule(
      LinkExtractor(
        allow=(item_pattern),
      ),
      follow=True,
      callback='parse_item'
    ),
    Rule(
      LinkExtractor(
        allow=(comment_pattern)
      ),
      callback='parse_comment'
    ),
  ]

  def parse_list(self, response):
    self.log('列表: %s' % response.url)

  def parse_item(self, response):
    self.log('药物详情: %s' % response.url)
    sel = Selector(response)
    drug = parse_drug_item(sel)
    # print(drug)
    # item = DrugItem()
    # item['approval_number'] = ''
    # yield item

  def parse_comment(self, response):
      self.log('药物评价: %s' % response.url)
      sel = Selector(response)
      comments = parse_drug_comments(sel)
      # print(comments[0])
      # list(map(lambda comment:

      # , comments))


      item = DrugComment()
      # item.duration
      yield item