import re
import time
import schedule
# import pymongo
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
from listweb import dict_data
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import ActionChains
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver_linux64/chromedriver', chrome_options=options)
actions = ActionChains(driver)
options.add_argument('--headless')

from script.connect import ConnectMongo
connect = ConnectMongo()
db = connect.db
db_new = connect.db_new

compile_regex = re.compile(r'(Nguồn):? (http://.*)|>>XEM THÊM:.*|\(.*\)\s?-\s|\(.*\)\s?–| NDĐT - ')

def get_info(link, xpath_title, xpath_content, xpath_time, xpath_tag):
    title = ''
    content = ''
    time_article = ''
    public_date = 0
    arr_tag = []
    time.sleep(5)
    driver.get(link)
    time.sleep(5)
    title = driver.find_element_by_xpath(xpath_title).text

    try:
        for _ in xpath_content:
            arr_content = driver.find_elements_by_xpath(_)
            for elem in arr_content:
                content += (' '+ elem.text)
        content = re.sub('\s\s+', ' ', content)
        content = compile_regex.sub('',content)

    except:
        content = ''
    
    time_article = driver.find_element_by_xpath(xpath_time).text
    time_article = re.sub(r'([^0-9\s:]+?)', '', time_article).strip()
    arr_time = time_article.split(' ')
    date_article = [elem for elem in arr_time if len(elem) >=4 and elem.find(':')<0][0]
    hour_article = [elem for elem in arr_time if elem.find(':')>=0][0]
    time_article = date_article + ' ' + hour_article
    try:
        public_date = datetime.strptime(time_article, '%d%m%Y %H:%M')
        public_date = public_date.timestamp() * 1000
    except:
        try:
            public_date = datetime.strptime(time_article, '%d%m%Y %H:%M:%S')
            public_date = public_date.timestamp() * 1000
        except:
            public_date = ''
    try:
        arr_tag = driver.find_elements_by_xpath(xpath_tag)
        for elem in arr_tag:
            tag += (elem.text.strip() +'#')
        tag = tag.replace('##', '#')
    except:
        tag = ''
    
    # driver.close()
    # driver.quit()
    return title, content, time_article, date_article, public_date, tag

def insert_data(final_time):
    myquery = { "now_time": { "$gt": final_time } }
    data = db_new.covid_news.find(myquery)
    N = data.count()
    print("tong doc", N)

    for _ in data:
        link_web = _['website']
        link = _['link']
        key = _['key']
        now_time = _['now_time']
        try:
            xpath_article = [value for web, value in dict_data.items() if web == link_web or web == link_web + '/']
            xpath_title, xpath_content, xpath_time, xpath_tag = xpath_article[0][0], xpath_article[0][1], xpath_article[0][2], xpath_article[0][3]

            item_article = {}
            title = ''
            content = ''
            time_article = ''
            tag = ''
            outlink = []
            # if mem > 500:
            try:
                title, content, time_article, date_article, public_time, tag = get_info(link, xpath_title, xpath_content, xpath_time, xpath_tag)
                # print({'website':link_web, 'key':key, 'link':link, 'now_time':now_time, 'title':title, 'content':content, 'tag':tag, 'date_article':date_article, 'public_time':public_time, 'time_article':time_article})
                db_new.articles.insert_one({'website':link_web, 'key':key, 'link':link, 'now_time':now_time, 'title':title, 'content':content, 'tag':tag, 'date_article':date_article, 'public_time':public_time, 'time_article':time_article})
            except:
                pass
        except:
            pass
            
def main():
    # final_time = 0
    # insert_data(final_time)
    last_doc = db_new.articles.find().sort([("_id", -1)]).limit(1)
    final_time = last_doc[0]['now_time']
    # print(final_time)
    try:
        insert_data(final_time)
    except:
        pass

if __name__ == "__main__":
    main()
    driver.close()
    driver.quit()
    # data = db.articles_final.find()
    # for _ in data:
    #     try:
    #         db_new.articles.insert_one(_)
    #     except:
    #         pass

# schedule.every().hour.do(main)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
