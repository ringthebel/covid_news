import re
import regex
import math

from preprocess import *
from underthesea import word_tokenize

# from data_prep import TextPreprocess
from script.connect import *

connect = ConnectMongo()
db = connect.db

connectTXT = ConnectTXT()

# compile_regex = re.compile(r'(Nguồn):? (http://.*)|>>XEM THÊM:.*|\(.*\)\s?-\s|\(.*\)\s?–| VOV.VN - | Kinhtedothi - | Bnews | VTV.vn - | TPO -| TP -| TGVN. | Ảnh:| TTO - ')
# regex = re.compile(r'[\?|!|@|#|$|%|^|&|\*|\(|\)|_|-|\+|=|,|.|:|...|..|\-|\/]')
# number1 = r'[\d.]+[ ]?[-–]?[ ]?[\d.]+\w*[°]?'  # for almost cases except 1kg, 2mm
# number2 = r'\d[°]?\w*'  # for vd: 1kg, 2mm
# date1 = r'\d{1,2}[-/]\d{1,2}[-/](?:\d{2}){1,2}'
# date2 = r'[^0-9]\d{1,2}[-/]\d{4}[^0-9]'
# date3 = r'[^0-9]\d{1,2}[/]\d{1,2}[^0-9]'
# date4 = r'[^0-9]\d{4}[-/]\d{2}[^0-9]'  # vd : 2018/19
# Np = r'[A-Za-z]+[-–][A-Za-z]+'
# ratio = r'NUM[ ]?%'
# dot = r'[.,:;?!…]'
# data_04 = db.articles.find({'date_article':{'$regex':r'\d+042020'}})
# def clean_doc(text):
#     # str_sub = compile_regex.sub('', text)
#     str_sub = re.sub(date1, "", text)
#     # print('date', str_sub)
#     str_sub = re.sub(date2, "", str_sub)
#     # print('date', str_sub)
#     str_sub = re.sub(date3, "", str_sub)
#     # print('date', str_sub)
#     str_sub = re.sub(date4, "", str_sub)
#     # print('date', str_sub)
#     str_sub = re.sub(number1, "", str_sub)
#     # print('num1', str_sub)
#     str_sub = re.sub(number2, "", str_sub)
#     # print('num2', str_sub)
#     str_sub = re.sub(Np, "", str_sub)
#     str_sub = re.sub(Np, "", str_sub)  # for some words type as A-B-C
#     # print('np', str_sub)
#     str_sub = re.sub(ratio, "", str_sub)
#     # print('ratio', str_sub)
#     str_sub = re.sub(dot, "", str_sub)

#     str_sub = re.sub(r'\s+', ' ', str_sub)
#     return str_sub

def get_listdoc(doc):
    arr_doc = doc.split(' ')
    return arr_doc

def mapper():
    N = data_04.count()
    DF = {}
    data_vocab = connectTXT.read_data('data/vocab.txt')
    vocab = data_vocab.split('\n')[:-1]
    for w in vocab:
        try:
            DF[w].add(id)
        except:
            DF[w] = {id}
    DF_term = {}
    for i in DF:
        DF_term[i] = math.log(N/(len(DF[i])+1))
    return DF, DF_term, vocab

def cal_tf(term, arr_doc):
    count_term = arr_doc.count(term)
    return count_term/len(arr_doc)

def reducer():
    result = mapper()
    DF_term, vocab_terms = result[1], result[2]
    # data = db.articles.find({'date_article':{'$regex':r'\d+052020'}})
    print(len(vocab_terms))

    for elem in data_04:
        id = elem['_id']
        content = elem['content']
        date_article = elem['date_article']
        content = compile_regex.sub('', content)
        content = regex.sub(' ', content)
        content = content.lower()
        content = clean_doc(content)
        arr_words = word_tokenize(content)
        vocab = list(set(arr_words))
        print(len(vocab))
        if len(vocab)>0:
            for w in vocab_terms:
                tf = cal_tf(w, vocab)
                idf = DF_term[w]
                if tf > 0:
                    print(w)
                    db.invert.insert_one({'term':w, 'id_doc':id, 'tfidf':tf*idf, 'date_article':date_article})
        print("===============================")
    

def write_vocab():
    data = db.articles.find({'date_article':{'$regex':r'\d+052020'}})
    N = data.count()
    print("so luong", N)
    DF = {}
    vocab = []
    for elem in data:
        id = elem['_id']
        content = elem['content']
        content = compile_regex.sub('', content)
        content = regex.sub(' ', content)
        content = content.lower()
        content = clean_doc(content)
        arr_words = word_tokenize(content)
        # print(arr_words)
        vocab += arr_words
        vocab = list(set(vocab))
    for w in vocab:
        connectTXT.write_data('data/vocab05.txt', w)

def build_vocab():
    vocab = []
    data_vocab1 = connectTXT.read_data('data/vocab01.txt')
    vocab1 = data_vocab1.split('\n')[:-1]
    data_vocab2 = connectTXT.read_data('data/vocab02.txt')
    vocab2 = data_vocab1.split('\n')[:-1]
    data_vocab3 = connectTXT.read_data('data/vocab03.txt')
    vocab3 = data_vocab1.split('\n')[:-1]
    data_vocab4 = connectTXT.read_data('data/vocab04.txt')
    vocab4 = data_vocab1.split('\n')[:-1]
    data_vocab5 = connectTXT.read_data('data/vocab05.txt')
    vocab5 = data_vocab1.split('\n')[:-1]
    vocab = vocab1+vocab2+vocab3+vocab4+vocab5
    vocab = list(set(vocab))
    for w in vocab:
        if len(w) > 1:
            connectTXT.write_data('data/vocab.txt', w)

reducer()