#配置debug工具调试文件
_author_='wuyifei'

from scrapy.cmdline import execute

import sys
import os

#print(os.path.dirname(os.path.abspath(__file__)))

#使用绝对路径
#sys.path.append("/home/wuyifei/app/ArticleSpider");

#使用相对路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])