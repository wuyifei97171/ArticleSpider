# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
from scrapy.loader import ItemLoader

#导入对url的转换工具类
from ArticleSpider.utils.common import get_md5

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2.获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数

        :param response:
        :return:
        """
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")

        for post_node in post_nodes:
            #使用join对response.url + post_url进行url的拼接
            #使用yield 让scrapy进行解析
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            #parse.urljoin 当传递进来的post_url没有域名，就使用response_url
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy集你想年下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self,response):
        article_item = JobBoleArticleItem() #实例化


        #提取文章的具体字段
        # re_selector = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()')
        # re_selector2 = response.xpath("/html/body/table/tbody/tr[350]/td[2]/span")
        # title = re_selector3 = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0].strip().replace("·","").strip()
        # praise_nums = int(response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])
        # fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # match_re = re.match(".*(\d+).*",fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0              由于在Item中进行处理了，所以这边的代码可以去掉了

        # comment_nums = response.xpath("//a[@href='#article-comment']/span").extract()[0]
        # match_re = re.match(".*(\d+).*",comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0          由于在Item中进行处理了，所以这边的代码可以去掉了
        # content = response.xpath("//div[@class='entry']").extract()[0]
        # create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        #
        # tag_list = response.xpath("//a[@href='#article-comment']/span").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)

        #向实例化数值赋值
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     #将create_date转换成date格式
        #     create_date = datetime.datetime.strptime(create_date,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()    #获取当前日期

        # article_item["create_date"] = create_date
        # article_item["url_object_id"] = get_md5(response.url)
        # 注意：这里的url要url转换成list
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        #通过item loader加载item
        #文章封面图
        #使用get方法请求，传递个默认值 空
        front_image_url = response.meta.get("front_image_url","")

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(),response=response)
        item_loader.add_css("title",".entry-header h1::text")
        #直接通过response取到的值 可以通过add_value获取
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_xpath("create_date","//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_value("front_image_url",[front_image_url])
        item_loader.add_xpath("praise_nums","//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_css("comment_nums","a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums",".bookmark-btn::text")
        item_loader.add_css("tags","p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content","div.entry")

        #调用item_loader的load_item方法，解析之前添加的规则，并传入article_item
        article_item = item_loader.load_item()
        #这里调用yield之后，这个item会传递到pipline中，注意需要在settings.py中把注释掉的pipelines代码取消注释
        yield article_item
        #通过css选择其提取字段
        # title = response.css(".entry-header h1::text").extract()[0]
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract()
        # praise_nums = response.css(".vote-post-up h10::text").extract()[0]
        # fav_nums = response.css(".bookmark-btn::text").extract()[0]
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract()
        # match_re = re.match(".*?(\d+).*",comment_nums)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        #
        # content = response.css("div.entry").extract()[0]
        #
        # tags = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        pass
