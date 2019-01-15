# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# 药物分类
# icon1: 甲类非处方药。不须医生处方就可以购买和出售，但必须在药店出售，并在药师指导下使用。
# icon2: 乙类非处方药。有着长期安全使用的记录，可以像普通商品一样在超市、杂货店直接出售。
# icon3: 处方药
# icon4: 国家基本药物是指由政府制定的《国家基本药物目录》中的药品。国家基本药物的遴选原则为：临床必需、安全有效、价格合理、使用方便、中西药并重。
# icon5: 医保药品甲类
# icon6: 中药保护品种二级
# icon9: 该产品为外用，请勿内服！
# icon12: 医保药品乙类。报销限制条件：限小儿发热惊风
# icon13: 条码已在中国物品编码中心注册
#

class DrugItem(Item):
    # 批准文号
    approval_number = Field()
    # 关联的平台药品ID
    drug_id = Field()
    # 药物名称
    name = Field()
    # 药物英文名
    name_en = Field()
    # 批准日期
    approval_date = Field()
    # 生产公司
    company = Field()
    telephone = Field()
    address = Field()
    # 剂型
    formulation = Field()
    # 规格
    specification = Field()
    # 有效期
    validity_period = Field()
    # 储存
    storage = Field()
    # 成分
    composition = Field()
    # 参考价格
    price = Field()
    # 主治功能
    indications = Field()
    # 用法用量
    dosage = Field()
    # 相关标签
    tags = Field()

class DrugComment(Item):
    # 批准文号，关联
    approval_number = Field()
    # 关联的平台药品ID
    drug_id = Field()
    # 关联的平台评论ID
    comment_id = Field()
    # 疗效
    efficacy_level = Field()
    # 副作用
    side_effect_level = Field()
    # 价格
    price_level = Field()
    # 评论
    comment = Field()
    # 地址
    address = Field()
    # 年龄
    age = Field()
    # 性别
    gender = Field()
    # 次数
    times = Field()
    # 持续时间
    duration = Field()
    # 提交时间
    submit_time = Field()