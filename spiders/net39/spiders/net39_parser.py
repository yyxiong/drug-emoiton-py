import re
import datetime
from scrapy.selector import Selector

def get_item_left_value(sel, attr):
  cite = sel.xpath('//div[@class="gs_left"]/ul//li/cite[text() = "%s"]' % attr)
  value = cite.xpath('./following-sibling::text()').extract_first()
  option = cite.xpath('.//option').extract_first()
  return option if option is not None else value

def get_item_right_value(sel, attr):
  dom_strong = sel.xpath('//div[@class="gs_right"]/div[@class="ps"]/p/strong[normalize-space(text()) = "%s"]' % attr)
  return dom_strong.xpath('./following-sibling::text() | ./following-sibling::a/text()').extract_first()

def get_tags(sel):
  return sel.xpath('//div[@class="gs_right"]/div[@class="related_tips"]/div/a/text()').extract()

# def get_drug_name(sel):
#   value = sel.xpath('//div[@class="yps_top"]//h1/a/text()').extract()
#   return ''.join(value)

# def get_company(sel, attr):
#   value = sel.xpath('//div[@class="yps_top"]/ul//li[@class="%s"]/a/text()' % attr).extract()
#   return ''.join(value)

def get_company_value(dom_top, attr):
  value = dom_top.xpath('./ul//li[@class="%s"]/text()' % attr).extract()
  return ''.join(value)

# def get_comment_href(sel):
#   value = sel.xpath('//div[@class="yps_top"]/div[@class="t4"]/ul/li/a[text()="用药经验"]/@href').extract()
#   return ''.join(value)

def parse_drug_item(response):
  sel = Selector(response)
  approval_number = get_item_left_value(sel, '批准文号：')
  approval_date = get_item_left_value(sel, '批准日期：')
  composition = get_item_right_value(sel, '成\xa0\xa0分')
  indications = get_item_right_value(sel, '功能主治')
  dosage = get_item_right_value(sel, '用法用量')

  dom_top = sel.xpath('//div[@class="yps_top"]')
  name = ''.join(dom_top.xpath('./div[@class="t1"]/h1/a/text()').extract())
  tags = get_tags(sel)
  company = ''.join(dom_top.xpath('ul/li[@class="company"]/a/text()').extract())
  address = get_company_value(sel, 'address')
  telephone = get_company_value(sel, 'telephone')
  drug_id = parse_drug_id(response.url, isIndex=True)
  return {
    'drug_id': drug_id,
    'name': name,
    'tags': tags,
    'approval_number': approval_number,
    'approval_date': approval_date,
    'composition': composition,
    'indications': trim(indications),
    'dosage': dosage,
    'company': company,
    'address': address,
    'telephone': telephone
  }

def trim(str):
  return re.sub(r'[ \t\r\n\xa0]', '', str) if str else ''

def parse_user(str):
  user = trim(str).lstrip('来自')
  res = re.search(r'((?!男|女)\S+)([男|女])((\d+)岁)?(第(\d+)次用药持续(\d+)天)?', user)
  if res:
    address = res.group(1)
    gender = res.group(2)
    age = res.group(4)
    times = res.group(6)
    duration = res.group(7)
    return {'address': address, 'gender': gender, 'age': age, 'times': times, 'duration': duration}
  else:
    return {'address': user}

def parse_submit_time(str):
  date = str.lstrip('点评时间：')
  return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M:%S')

def parse_levels(arr):
  return list(map(lambda level: level.lstrip('star_new star_new'), arr))

def parse_drug_comment(box):
  boxTop = box.xpath('.//div[@class="pls_top"]')
  user_str = boxTop.xpath('.//cite/text()').extract_first()
  submit_time = boxTop.xpath('.//i/text()').extract_first()
  boxMid = box.xpath('.//div[@class="pls_mid"]')
  levels = boxMid.xpath('./ul//li/span/@class').extract()
  comment = boxMid.xpath('./p/text()').extract_first()
  comment_id = box.xpath('.//div[@class="pls_bot"]//form/input[@name="DrugCommentsId"]/@value').extract_first()

  user = parse_user(user_str)
  return {
    # 'user': user,
    **user,
    'submit_time': parse_submit_time(submit_time),
    'efficacy_level': parse_levels(levels),
    'comment': comment,
    'comment_id': comment_id
  }

def parse_drug_id(url, isIndex = False):
  pattern = r'/(\d+)/$' if isIndex else r'/(\d+)/comment'
  res = re.search(pattern, url)
  return res.group(1)

def parse_drug_comments(response):
  sel = Selector(response)
  drug_id = parse_drug_id(response.url)
  boxs = sel.xpath('//div[@class="pls"]//div[@class="pls_box"]')
  return [drug_id, list(map(parse_drug_comment, boxs))]
