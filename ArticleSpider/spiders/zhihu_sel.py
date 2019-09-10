
def start_requests(self):
    return [scrapy.Request]

    from selenium import webdriver
    firefox_driver_path = "/home/wuyifei/app/ArticleSpider/geckodriver"
    brower = webdriver.Firefox(executable_path=firefox_driver_path)

    brower.get("https://www.zhihu.com/signin")
    brower.find_element_by_css_selector('.SignFlow-accountInput Input-wrapper input[value name="username"]')\
        .send_keys("15618911316")
    brower.find_element_by_css_selector('.SignFlow-password.SignFlowInput.Input-wrapper input[value name="password"]')\
        .send_keys("123123123")
    brower.find_element_by_css_selector('.Button SignFlow-submitButton Button--primary Button--blue').click()

    import time
    time.sleep(10)
    Cookies = brower.get_cookies()
    print(Cookies)
    cookie_dict = {}
    import pickle
    for cookie in Cookies:
        #写入文件
        f = open('/home/wuyifei/app/ArticleSpider/cookies/zhihu/'+cookie['name']+'.zhihu','wb')
        pickle.dump(cookie,f)
        cookie_dict[cookie['name']] = cookie['value']
    brower.close()
    return [scrapy.Request(url=self.start_urls[0],)]
