import time
import sys
import re
import schedule
import psutil

from datetime import datetime
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse
# from marks import parse_sent_true, parse_sent_one
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--headless')

from script.connect import ConnectMongo
connect = ConnectMongo()
db = connect.db

driver = webdriver.Chrome('chromedriver_linux64/chromedriver', chrome_options=options)

regex_content = re.compile(r'(\(.*\)\s?-\s)get_ncov(final_time)|(\(.*\)\s?–)')

def get_ncov(final_time):
    link_cddh = 'https://ncov.moh.gov.vn/web/guest/chi-dao-dieu-hanh?p_p_id=101_INSTANCE_iEPhEhL1XSde&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=_118_INSTANCE_IrnCPpeHzQ4m__column-1&p_p_col_count=1&_101_INSTANCE_iEPhEhL1XSde_delta=5&_101_INSTANCE_iEPhEhL1XSde_keywords=&_101_INSTANCE_iEPhEhL1XSde_advancedSearch=false&_101_INSTANCE_iEPhEhL1XSde_andOperator=true&p_r_p_564233524_resetCur=false&_101_INSTANCE_iEPhEhL1XSde_cur={}'
    for i in range(10):
    # for i in range(1):
        mem_dict = dict(psutil.virtual_memory()._asdict())
        if mem_dict.get("available") / 1048576 > 1000:
            url = link_cddh.format(i+1)
            # url = 'https://ncov.moh.gov.vn/web/guest/-/phong-chong-dich-covid-19-siet-chat-quan-ly-to-bay-cho-y-kien-ve-du-lich-quoc-te'
            driver.get(url)
            time.sleep(5)
            div_content = driver.find_elements_by_xpath('//div[@class="portlet-body"]//a')
            list_links = [elem.get_attribute('href') for elem in div_content if elem.get_attribute('href').find('https://ncov.moh.gov.vn/web/guest/chi-dao-dieu-hanh')<0 and  elem.get_attribute('href').find('https://ncov.moh.gov.vn/') == 0]
            for link in list_links:
                driver.get(link)
                time.sleep(5)
                
                try:
                    time_article = driver.find_element_by_xpath('.//span[@class="text-ngayxam-page"]').text
                    time_article = re.sub(r'([^0-9\s:\/]+?)', '', time_article).strip()
                    date_article = time_article[:10].replace('/', '')
                except:
                    date_article = ''
                try:
                    public_date = datetime.strptime(time_article, '%d/%m/%Y %H:%M')
                    public_date = public_date.timestamp() * 1000
                
                    if public_date > final_time:
                        # try:
                        content = driver.find_element_by_xpath('//div[@class="journal-content-article"]').text
                        arr_sents = parse_sent_one(content)
                        for sent in arr_sents:
                            dic_article = {'website':'https://ncov.moh.gov.vn', 'link':link, 'sent_text':sent[0], 'sent_day':sent[1], 'sent_mount':sent[2], 'sent_BN':sent[3], 'sent_w2v':sent[4], 'public_date':public_date, 'date_article':date_article}
                            db.articles_ncov_cddh.insert_one(dic_article)

                            # dic_article = {'website':'https://ncov.moh.gov.vn', 'link':link, 'arr_sents':arr_sents, 'public_date':public_date, 'date_article':date_article}
                            # db.articles_true.insert_one(dic_article)
                        # except:
                        #     print("no content")
                except:
                    public_date = 0
            
        else:
            print("whu")
            sys.exit()

def get_dtg(final_time):
    link_dtg = 'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian?p_p_id=101_INSTANCE_iEPhEhL1XSde&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=_118_INSTANCE_IrnCPpeHzQ4m__column-1&p_p_col_count=1&_101_INSTANCE_iEPhEhL1XSde_delta=30&_101_INSTANCE_iEPhEhL1XSde_keywords=&_101_INSTANCE_iEPhEhL1XSde_advancedSearch=false&_101_INSTANCE_iEPhEhL1XSde_andOperator=true&p_r_p_564233524_resetCur=false&_101_INSTANCE_iEPhEhL1XSde_cur={}'
    for i in range(10):
        mem_dict = dict(psutil.virtual_memory()._asdict())
        if mem_dict.get("available") / 1048576 > 1000:
            url = link_dtg.format(i+1)
            driver.get(url)
            time.sleep(5)
            arr_news = driver.find_elements_by_xpath('//div[@class="timeline-sec"]//ul//li')
            # print(len(arr_news))
            for elem in arr_news:
                try:
                    time_article = elem.find_element_by_xpath('.//div[@class="timeline-head"]/h3').text
                    date_article = time_article[6:].replace('/', '')
                except:
                    date_article = ''
                try:
                    public_date = datetime.strptime(time_article, '%H:%M %d/%m/%Y')
                    public_date = public_date.timestamp() * 1000
                    if public_date > final_time :
                        try:
                            content = elem.find_element_by_xpath('.//div[@class="timeline-content"]').text
                            arr_sents = parse_sent_true(content)
                            for sent in arr_sents:
                                dic_article = {'website':'https://ncov.moh.gov.vn', 'link':'', 'sent_text':sent[0], 'sent_day':sent[1], 'sent_mount':sent[2], 'sent_BN':sent[3], 'sent_w2v':sent[4], 'public_date':public_date, 'date_article':date_article}
                                # print(dic_article, "\n==========================")
                                db.articles_ncov_dtg.insert_one(dic_article)
                       
                        except:
                            print("can not insert")
                    else:
                        pass
                except:
                    public_date = 0
            
            # driver.close()
            # driver.quit()
        else:
            print("whu")
            sys.exit()
        
def main():
    last_doc = db.articles_ncov_dtg.find().sort([("public_date", -1)]).limit(1)
    final_time = last_doc[0]['public_date']
    last_doc_cddh = db.articles_ncov_cddh.find().sort([("public_date", -1)]).limit(1)
    final_time_cddh = last_doc_cddh[0]['public_date']
    # # final_time = 15897996000010.0
    get_ncov(final_time_cddh)
    get_dtg(final_time)
    driver.close()
    driver.quit()
    # # get_dtg(final_time)

    # data_dtg = db.articles_ncov_dtg.find({},{'_id':0})
    # data_cddh = db.articles_ncov_cddh.find({},{'_id':0})
    # for elem in data_dtg:
    #     db.articles_ncov.insert_one(elem)
    # for elem in data_cddh:
    #     db.articles_ncov.insert_one(elem)
main()