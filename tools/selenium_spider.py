from selenium import webdriver
from scrapy.selector import Selector

firefox_driver_path = "/home/wuyifei/app/ArticleSpider/geckodriver"
brower = webdriver.Firefox(executable_path=firefox_driver_path)

web_url = "http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html"
brower.get(web_url)

# print(brower.page_source)
#
# t_selector = Selector(text=brower.page_source)
# print(t_selector.css(".tb-rmb-num::text").extract())
# brower.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[1]/td[2]/input').send_keys('0205772999999')
# brower.find_element_by_xpath('/html/body/form/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]/input').send_keys('bcwh123456')



# brower.quit()