# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
import time
import re

from marks import *
from script.connect import ConnectMongo
connect = ConnectMongo()
db = connect.db
db_old = connect.db_old

def get_score(data):
    artile_id = data['_id']
    link = data['link']
    content = data['content']
    content_color = content
    title = data['title']
    date_article = data['date_article']
    now_time = data['now_time']
    time_article = data['time_article']
    list_id_matching = []
    data_matching = db.articles_ncov.find({'date_article':date_article})    
    parse_sent = parse_sent_one(content)
    import copy
    for elem in parse_sent[:]:
        elem_sent = elem[0]
        elem_date = elem[1]
        elem_num = elem[2]
        elem_BN = elem[3]
        elem_w2v = elem[4]
        arr_sims = []
        temp = copy.deepcopy(data_matching)
        for elem_matching in temp:
            id_matching = elem_matching['_id']
            matching_sent = elem_matching['sent_text']
            matching_date = elem_matching['sent_day']
            matching_num = elem_matching['sent_mount']
            matching_BN = elem_matching['sent_BN']
            matching_w2v = elem_matching['sent_w2v']
            cos_sim = dot(elem_w2v, matching_w2v)/(norm(elem_w2v)*norm(matching_w2v))
            arr_sims.append({'sim':cos_sim, 'data': [matching_sent, matching_date, matching_num, matching_BN, id_matching]})
        if len(arr_sims) > 0:
            od = sorted(arr_sims, key=lambda k: k['sim'])[-1]
            sim_max = od['sim']
            sent_matching = od['data']
            id_matching_max = sent_matching[-1]
            if 0.91 < sim_max and sim_max <= 1:
                # format_sent = '{}'+
                sent_green = '<font color="#4da6ff">' + elem_sent + '</font>'
                content = content.replace(elem_sent, sent_green) #chua chi ra dc id bai cua ncov
                list_id_matching.append(['green',elem_sent, id_matching_max])
            elif 0.8 < sim_max and sim_max <= 0.91:
                sent = sent_matching[0]
                date = sent_matching[1]
                num = sent_matching[2]
                BN = sent_matching[3]
                phraise1, list_day1, phraise_BN1 = check_sent(elem_sent, elem_date, elem_num, elem_BN)
                phraise2, list_day2, phraise_BN2 = check_sent(sent, date, num, BN)
               
                for i in phraise_BN1:
                    if i in phraise_BN2:
                        BN_green = '<font color="#4da6ff">' + i + '</font>'
                        content_color = content_color.replace(i, BN_green)
                        list_id_matching.append([ 'green', i, id_matching_max])
                    else:
                        BN_red = '<font color="#ff4d4d">' + i + '</font>'
                        content_color = content_color.replace(i, BN_red)
                        list_id_matching.append(['red', i, id_matching_max])
                    
                for i in range(len(phraise1)):
                    if phraise1[i] in phraise2:
                        sub_num = elem_sent[elem_num[i][0]:elem_num[i][1]-1]
                        num_green = '<font color="#4da6ff">' + sub_num + '</font>'
                        content_color = content_color.replace(sub_num, num_green)
                        list_id_matching.append(['green', sub_num, id_matching_max])
                    if phraise1[i] in phraise2:
                        sub_num = elem_sent[elem_num[i][0]:elem_num[i][1]-1]
                        num_red = '<font color="#ff4d4d">' + sub_num + '</font>'
                        content_color = content_color.replace(sub_num, num_red)
                        list_id_matching.append(['red', sub_num, id_matching_max])
                    
                for i in list_day1:
                    if i in list_day2:
                        day_green = '<font color="4da6ff">' + i + '</font>'
                        content_color = content_color.replace(i, day_green)
                        list_id_matching.append(['green', i, id_matching_max])
                    else:
                        day_red = '<font color="#ff4d4d">' + i + '</font>'
                        content_color = content_color.replace(i, day_red)
                        list_id_matching.append(['red', i, id_matching_max])
                    
            else:
                print("khong boi mau")
                pass
        else:
            pass
    if len(list_id_matching) > 0:
        dic_content = {'artile_id':artile_id, 'link':link, 'title': title, 'content':content, 'content_color':content_color, 'now_time':now_time, 'time_article':time_article, 'list_id_matching':list_id_matching}
        db.articles_colors_final.insert_one(dic_content)
    
def main():
    last_doc = db.articles_colors.find().sort([("_id", -1)]).limit(1)
    final_time = last_doc[0]['now_time']
    myquery = { "now_time": { "$gt": final_time } }
#     myquery = {}
    list_data = db.articles_final.find(myquery)
    print(list_data.count())
    for data in list_data[:]:
        get_score(data)
        time.sleep(10)
main()
