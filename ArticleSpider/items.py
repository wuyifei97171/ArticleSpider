# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader
import re
class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value+"-bobby"


def date_convert(value):
    try:
        # 将create_date转换成date格式
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()  # 获取当前日期
    return create_date


def get_nums(value):
    match_re = re.match(".*(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    #取消tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value

def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    #自定义itemLoader，目的是让抓取到的值 统一从list转成str或者其他形式
    default_output_processor = TakeFirst()

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        #使用input_processor 对传递到title中的值进行预处理
        # input_processor = MapCompose(add_jobbole)
        input_processor = MapCompose(lambda x:x+"-jobbole",add_jobbole) #除了使用上面的函数，也可以使用lambda函数,以此调用两个函数

    )

    create_date = scrapy.Field(
        input_processor = MapCompose(date_convert),
        # output_processor = TakeFirst()  #使用takeFirst()取出第一个数值,由于使用了自定义的ItemLoader来进行takeFirst,所以不用这边操作了
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()      #将url进行MD5转换，变为定长
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)   #将List中的第一个值提取出来
    )
    front_image_path = scrapy.Field()   #本地的图片存储路径
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()