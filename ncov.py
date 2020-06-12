import re
import time
import schedule
import pymongo
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
from listweb import dict_data
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver_linux64/chromedriver', chrome_options=options)
actions = ActionChains(driver)
# options.add_argument('--headless')

from script.connect import ConnectMongo
connect = ConnectMongo()
db = connect.db
db_new = connect.db_new

driver = webdriver.Chrome('chromedriver_linux64/chromedriver', chrome_options=options)
actions = ActionChains(driver)

keys = [
    "toàn dân đoàn kết hậu covid",
    "doanh nghiệp có thể phá sản nếu covid kéo dài",
    "lợi ích dịch covid mang lại",
    "người dân chủ quan trong phòng chống dịch"
    "corona làm suy thoái kinh tế ",
    "vắc xin cho corona",
    "khẩu trang mùa covid",
    "các gói cứu trợ cho kinh tế việt nam",
    "khu cách ly mùa dịch covid",
    "các ca hồi phục khỏi covid tại việt nam",
    "đóng góp của cộng đồng mùa dịch",
    "tiếp tục phòng chống dịch",
    "nghĩa cử cao đẹp mùa dich",
    "câu chuyện mùa dịch",
    "khó khăn mà doanh nghiệp gặp phải",
    "dịch covid và bầu cử tại Mỹ",
    "tin tức covid 19",
    "tin giả covid",
    "tình hình covid tại Mỹ",
    "tình hình covid tại các nước châu Âu",
    "triệu trứng corona"
    ]
# txt_site = 'or'.join(list_web)
def get_links():
    arr_links_page = []
    try:
        first_link = driver.find_element_by_id('n1s0p1c0').get_attribute('href')
        arr_links_page.append(first_link)
    except:
        pass
    try:
        arr_links = driver.find_elements_by_xpath('//div[@id="rso"]//div[@class="r"]/a')
        arr_links_page = [elem.get_attribute('href') for elem in arr_links]
    except:
        pass
    return arr_links_page

# nextpage of google.com
def next_page():
    div_next = driver.find_elements_by_xpath('//a[@class="G0iuSb"]')
    link_next = [elem.get_attribute('href') for elem in div_next]
    texts = [elem.text for elem in div_next]
    if texts[-1] == 'Tiếp':
        url = link_next[-1]
        time.sleep(10)
        driver.get(url)
        if url.find('https://www.google.com/search?') == 0:
            return 1
        else:
            return 0
    else:
        return 0

# check url can be crawl 
def check_url(url):
    url_parse = urlparse.urlparse(url)
    web = url_parse.scheme+'://'+url_parse.netloc
    if len(url_parse.path) > 40 and web != 'https://www.youtube.com':
        return web
    else:
        return 0
   
def main():
    try:
        url = 'https://www.google.com/'

        posts = db_new.covid_news

        for key in keys:
            time.sleep(5)
            driver.get(url)
            time.sleep(5)
            find = driver.find_element_by_name('q')
            find.send_keys(key)
            find.send_keys(Keys.RETURN) 
            i = 1
            while i<7:
                arr_links_page = get_links()
                arr_links_page = list(set(arr_links_page))
                for link in arr_links_page:
                    check = check_url(link)
                    if check:
                        try:
                            post_id = posts.insert_one({"key":key, "website":check, "now_time":time.time()*1000, "link":link}).inserted_id
                            print(post_id, "\n===================")
                        except:
                            pass
                    else:
                        print("no", link)
                
                i += next_page()
                print("value i ", i)
                time.sleep(10)
    except:
        pass

# schedule.every().hour.do(main)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

if __name__ == "__main__":
    # data = db.covid_new.find()
    # for _ in data:
    #     try:
    #         db_new.covid_news.insert_one(_)
    #     except:
    #         pass
    t1 = time.time()
    main()
    # driver.close()
    # driver.quit()
    print(time.time()-t1)