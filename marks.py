import re
import time
import torch
import argparse
import numpy as np

from script.connect import ConnectMongo
connect = ConnectMongo()
db = connect.db

from underthesea import pos_tag
from underthesea import word_tokenize
from underthesea import sent_tokenize
from transformers import RobertaConfig
from fairseq.data.encoders.fastbpe import fastBPE
# from sklearn.metrics.pairwise import cosine_similarity
from numpy import dot

from numpy.linalg import norm

from fairseq.data import Dictionary 
config = RobertaConfig.from_pretrained(
    "PhoBERT_base_transformers/config.json"
)
# Load BPE encoder 
parser_w2v = argparse.ArgumentParser()
parser_w2v.add_argument('--bpe-codes', 
    default="PhoBERT_base_transformers/bpe.codes",
    required=False,
    type=str,  
    help='path to fastBPE BPE'
)

from fairseq import options  
parser_mask = options.get_preprocessing_parser()  
parser_mask.add_argument('--bpe-codes', type=str, help='', default="PhoBERT_base_fairseq/bpe.codes")  

from vncorenlp import VnCoreNLP
rdrsegmenter = VnCoreNLP("VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx500m') 
vocab = Dictionary()
vocab.add_from_file("PhoBERT_base_transformers/dict.txt")
from transformers import RobertaModel
phobert_w2v = RobertaModel.from_pretrained(
    "PhoBERT_base_transformers/model.bin",
    config=config
)

from fairseq.models.roberta import RobertaModel
phobert_mask = RobertaModel.from_pretrained('PhoBERT_base_fairseq', checkpoint_file='model.pt')
phobert_mask.eval()

def token_sent(sent):
    sent_token = rdrsegmenter.tokenize(sent)
    return sent_token
    
def get_w2v_sent(arr_sent):
    # from transformers import RobertaModel
    # phobert_w2v = RobertaModel.from_pretrained(
    #     "PhoBERT_base_transformers/model.bin",
    #     config=config
    # )

    args = parser_w2v.parse_args()
    bpe = fastBPE(args)

    # Load the dictionary  
    # vocab = Dictionary()
    # vocab.add_from_file("PhoBERT_base_transformers/dict.txt")
    # line = "Tôi là sinh_viên trường đại_học Công_nghệ ."  
    line = ' '.join(arr_sent[0])
    # Encode the line using fastBPE & Add prefix <s> and suffix </s> 
    subwords = '<s> ' + bpe.encode(line) + ' </s>'

    # Map subword tokens to corresponding indices in the dictionary
    input_ids = vocab.encode_line(subwords, append_eos=False, add_if_not_exist=False).long().tolist()

    # Convert into torch tensor
    all_input_ids = torch.tensor([input_ids], dtype=torch.long)

    # Extract features  
    with torch.no_grad():  
        features = phobert_w2v(all_input_ids)  
    
    # Represent each word by the contextualized embedding of its first subword token  
    # i. Get indices of the first subword tokens of words in the input sentence 
    listSWs = subwords.split()  
    firstSWindices = []  
    for ind in range(1, len(listSWs) - 1):  
        if not listSWs[ind - 1].endswith("@@"):  
            firstSWindices.append(ind)  

    # ii. Extract the corresponding contextualized embeddings  
    vector_sent = []
    words = line.split()  
    assert len(firstSWindices) == len(words)  
    vectorSize = features[0][0, 0, :].size()[0]  
    for word, index in zip(words, firstSWindices):  
        vector_sent.append([features[0][0, index, :][_ind].item() for _ind in range(vectorSize)])
        # print(word, " --> " ,[features[0][0, index, :][_ind].item() for _ind in range(vectorSize)])
    result = np.array(vector_sent)
    result_vec = np.sum(result, axis=0)
    return result_vec

def mark(line, masked_line):
    # Load PhoBERT-base in fairseq
    # from fairseq.models.roberta import RobertaModel
    # phobert_mask = RobertaModel.from_pretrained('PhoBERT_base_fairseq', checkpoint_file='model.pt')
    # phobert_mask.eval()  # disable dropout (or leave in train mode to finetune)

    # Incorporate the BPE encoder into PhoBERT-base 
    args = parser_mask.parse_args() 
    phobert_mask.bpe = fastBPE(args) #Incorporate the BPE encoder into PhoBERT

    # INPUT TEXT IS WORD-SEGMENTED!
    # line = "Tôi là sinh_viên trường đại_học Công_nghệ ."  

    # Extract the last layer's features  
    subwords = phobert_mask.encode(line)  
    last_layer_features = phobert_mask.extract_features(subwords)  
    # assert last_layer_features.size() == torch.Size([1, 9, 768])  
    
    # Extract all layer's features (layer 0 is the embedding layer)  
    all_layers = phobert_mask.extract_features(subwords, return_all_hiddens=True)  
    assert len(all_layers) == 13  
    assert torch.all(all_layers[-1] == last_layer_features)  

    # Filling marks  
    # masked_line = 'Tôi là  <mask> trường đại_học Công_nghệ .'  
    topk_filled_outputs = phobert_mask.fill_mask(masked_line, topk=1)
    return topk_filled_outputs
    # print(topk_filled_outputs)

def get_similar(sent1, sent2):
    arr_1 = token_sent(sent1)
    arr_2 = token_sent(sent2)
    vec1 = get_w2v_sent(arr_1) #numpy.array
    vec2 = get_w2v_sent(arr_2)
    result = cosine_similarity(vec1.reshape(1,-1), vec2.reshape(1,-1))
    return result

# def parse_sent(website, link, key, now_time, title, tag, public_time, time_article, content):
def parse_sent(content):
    regex_day = '(\d+\/\d+)|(\d+\-\d+)'
    regex_num = '\s\d+\s'
    regex_BN = 'BN\d+'

    arr_sents = []
    arr_sents_token = sent_tokenize(content)
    for sent in arr_sents_token:
        # txt = sent.strip( )
        txt = sent
        date = [m.span() for m in re.finditer(regex_day, txt)]
        num = [m.span() for m in re.finditer(regex_num, txt)]
        BN = [m.span() for m in re.finditer(regex_BN, txt)]
        if len(num) > 0 or len(BN) > 0:
            arr = token_sent(txt)
            vec_sent = get_w2v_sent(arr).tolist()
            arr_sents.append([sent, date, num, BN, vec_sent])
        # else:
        #     vec_sent = []

        # arr_sents.append([sent, date, num, BN, vec_sent])
    return arr_sents

#danh rieng cho trang dong thoi gian, co cau: thong bao cua ...:
def parse_sent_true(content):
    regex_day = '(\d+\/\d+)|(\d+\-\d+)'
    regex_num = '\s\d+\s'
    regex_BN = 'BN\d+'

    arr_sents = []  
    ind = content.find(':')
    content = content[ind+2:]
    sents_token = []
    arr_sents_token = sent_tokenize(content)
    for elem in arr_sents_token:
        find = re.findall(';', elem) #tim ; voi tung cau
        if len(find) == 1:
            sents_token += elem.split(';')
        else:
            sents_token.append(elem)       
    for sent in sents_token:
        # txt = sent.strip( )
        txt = sent
        date = [m.span() for m in re.finditer(regex_day, txt)]
        num = [m.span() for m in re.finditer(regex_num, txt)]
        BN = [m.span() for m in re.finditer(regex_BN, txt)]
        if len(num) > 0 or len(BN) > 0:
            arr = token_sent(txt)
            vec_sent = get_w2v_sent(arr).tolist()
            arr_sents.append([sent, date, num, BN, vec_sent])
        # else:
        #     vec_sent = []

        # arr_sents.append([sent, date, num, BN, vec_sent])
    return arr_sents

def check_sent(sent, day, num, BN):
    #nhung cau co do tuong tu cao
    pos_tag_sent = pos_tag(sent)
    list_day = []
    phraise = []
    phraise_BN = []
    if len(num) > 0:
        for i in num:
            sub_sum = sent[i[0]:i[1]-1].strip(' ')
            sub_sent = sent[i[1]-1:]
            pos_tag_sub_sent = pos_tag(sub_sent)
            if pos_tag_sub_sent[0][1] != 'N':
                line = word_tokenize(sent, format="text")
                masked_line = word_tokenize(sent[:i[1]-1], format="text") + '  <mask> ' + word_tokenize(sent[i[1]-1:], format="text")
                result = mark(line, masked_line)
                phraise.append(sub_sum + ' ' + result)
            else:
                phraise.append(sub_sum + ' ' + pos_tag_sub_sent[0][0])

    if len(day) > 0:
        for i in day:
            sub_day = sent[i[0]:i[1]].strip(' ')
            sub_day = re.sub('-', '/', sub_day)
            list_day.append(sub_day)
    if len(BN) > 0:
        for i in BN:
            sub_BN = sent[i[0]:i[1]-1].strip(' ')
            phraise_BN.append(sub_BN)
    return phraise, list_day, phraise_BN

def parse_sent_one(content):
    regex_day = '(\d+\/\d+)|(\d+\-\d+)'
    regex_num = '\s\d+\s'
    regex_BN = 'BN\d+'

    arr_sents = []
    arr_sents_token = sent_tokenize(content)
    for sent in arr_sents_token:
        # txt = sent.strip( )
        txt = sent
        date = [m.span() for m in re.finditer(regex_day, txt)]
        num = [m.span() for m in re.finditer(regex_num, txt)]
        BN = [m.span() for m in re.finditer(regex_BN, txt)]
        if len(num) > 0 or len(BN) > 0:
            arr = token_sent(txt)
            vec_sent = get_w2v_sent(arr).tolist()
            arr_sents.append([sent, date, num, BN, vec_sent])
        # else:
        #     vec_sent = []

        # arr_sents.append([sent, date, num, BN, vec_sent])
    return arr_sents
    # vd: ngày 20/5 có 30 bênh nhân nhiễm covid

