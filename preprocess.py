import re

compile_regex = re.compile(r'(Nguồn):? (http://.*)|>>XEM THÊM:.*|\(.*\)\s?-\s|\(.*\)\s?–| VOV.VN - | Kinhtedothi - | Bnews | VTV.vn - | TPO -| TP -| TGVN. | Ảnh:| TTO - ')
regex = re.compile(r'[\?|!|@|#|$|%|^|&|\*|\(|\)|_|-|\+|=|,|.|:|...|..|\-|\/]')
number1 = r'[\d.]+[ ]?[-–]?[ ]?[\d.]+\w*[°]?'  # for almost cases except 1kg, 2mm
number2 = r'\d[°]?\w*'  # for vd: 1kg, 2mm
date1 = r'\d{1,2}[-/]\d{1,2}[-/](?:\d{2}){1,2}'
date2 = r'[^0-9]\d{1,2}[-/]\d{4}[^0-9]'
date3 = r'[^0-9]\d{1,2}[/]\d{1,2}[^0-9]'
date4 = r'[^0-9]\d{4}[-/]\d{2}[^0-9]'  # vd : 2018/19
Np = r'[A-Za-z]+[-–][A-Za-z]+'
ratio = r'NUM[ ]?%'
dot = r'[.,:;?!…]'

def clean_doc(text):
    # str_sub = compile_regex.sub('', text)
    str_sub = re.sub(date1, "", text)
    # print('date', str_sub)
    str_sub = re.sub(date2, "", str_sub)
    # print('date', str_sub)
    str_sub = re.sub(date3, "", str_sub)
    # print('date', str_sub)
    str_sub = re.sub(date4, "", str_sub)
    # print('date', str_sub)
    str_sub = re.sub(number1, "", str_sub)
    # print('num1', str_sub)
    str_sub = re.sub(number2, "", str_sub)
    # print('num2', str_sub)
    str_sub = re.sub(Np, "", str_sub)
    str_sub = re.sub(Np, "", str_sub)  # for some words type as A-B-C
    # print('np', str_sub)
    str_sub = re.sub(ratio, "", str_sub)
    # print('ratio', str_sub)
    str_sub = re.sub(dot, "", str_sub)

    str_sub = re.sub(r'\s+', ' ', str_sub)
    return str_sub
