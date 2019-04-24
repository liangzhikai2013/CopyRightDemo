# coding=utf-8

'''
    准备工作
'''

import codecs
import numpy as np
import os
import jieba
import jieba.analyse
import nltk
from nltk.translate.bleu_score import sentence_bleu
import time
import matplotlib.pyplot as plt
# from flask import jsonify

db_data = []
db_hash = []
db_doc_idx = {}
GENERATE_PATH = "/Users/lulu/Downloads/DuplicateChecking-master/result"
def hammingDis(simhash1, simhash2):  # 计算汉明距离
    t1 = '0b' + simhash1
    t2 = '0b' + simhash2
    n = int(t1, 2) ^ int(t2, 2)
    i = 0
    while n:
        n &= (n-1)
        i += 1
    # print("hammingDis() executed!")
    return i

def string_hash(source):
    if source == '':
        return 0
    else:
        x = ord(source[0]) << 7
        m = 1000003
        mask = 2 ** 128 - 1
        for c in source:
            x = ((x * m) ^ ord(c)) & mask
        x ^= len(source)
        if x == -1:
            x = -2
        x = bin(x).replace('0b', '').zfill(64)[-64:]
    # print("string_hash() executed!")
    return str(x)
    
def simhash(content):
    seg = jieba.lcut(content)  # 分词
    # print(seg)

    text=nltk.text.Text(jieba.lcut(content))
    # print(text.concordance(u'白鹿原'))
    # jieba.analyse.set_stop_words('/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/stopwords.txt')  # 去除停用词
    keyWord = jieba.analyse.extract_tags(
       '|'.join(seg), topK=100, withWeight=True, allowPOS=())
        # 在这里对 jieba 的 tfidf.py 进行了修改
        # 将 tags = sorted(freq.items(), key=itemgetter(1), reverse=True) 修改成 tags = sorted(freq.items(), key=itemgetter(1,0), reverse=True)
        # 即先按照权重排序，再按照词排序
    # print(keyWord)
    keyList = []
    strKeyWord = ''
    keyCount = 0
    for feature, weight in keyWord:  # 对关键词进行 hash

        strKeyWord += str(feature) + ':' + str(weight) + ' '
        weight = int(weight * 20)
        print(feature, weight)
        feature = string_hash(feature)

        temp = []
        for i in feature:
            if(i == '1'):
                temp.append(weight)
            else:
                temp.append(-weight)
       # print(temp)
        keyList.append(temp)
        keyCount += 1
        if keyCount <= 5:
            strKeyWord = ''
    list1 = np.sum(np.array(keyList), axis=0)
    if(keyList == []):  # 编码读不出来
        return strKeyWord, '00'
    simhash = ''
    for i in list1:  # 权值转换成 hash 值
        if(i > 0):
            simhash = simhash + '1'
        else:
            simhash = simhash + '0'
    # print("simhash() executed!")
    return strKeyWord, simhash

    
'''
    建立数据库
'''
def db_target_build():
    print("db_build() starting …")
    prepath = '/Users/lulu/Downloads/DuplicateChecking-master/target'
    doc_name = os.listdir(prepath)
    global db_target_hash,db_target_data# 全局变量
    db_target_data = []
    db_target_hash = []
    count = 0
    for name in doc_name:
        print(count, '\t', name)
        count += 1
        txt = np.loadtxt(codecs.open(os.path.join(prepath, name), encoding='utf-8',errors='ignore')
                        , dtype=np.str, delimiter="\r\n", encoding='utf-8')

        txtlist=list(map(lambda x:x.split("。"),txt))
        txtarray=[]
        for item in txtlist:

            item = np.array(item)
            txtarray = np.append(txtarray,item)
        txtarray = np.char.replace(txtarray, '\\u3000', '')
        txtarray = np.char.replace(txtarray, '\\u3000\\u3000', '')

        for paragraph in txtarray:
            if paragraph == '' or paragraph == ' ' or paragraph.find(' ') != -1 or paragraph[0].isdigit():
                continue
            strKeyWord, shash = simhash(paragraph)
            if strKeyWord == '':
                continue
            db_target_data.append([name, paragraph, strKeyWord])
            db_target_hash.append(shash)
    print("db_save() starting …")

    db_target_data = np.array(db_target_data)
    db_target_hash = np.array(db_target_hash)
    np.save("/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_target_data.npy", db_target_data)
    np.save("/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_target_hash.npy", db_target_hash)
    print(db_target_data)
    print(db_target_hash)
    print("*****************")
    print("db_save() executed!")

    print("db_build() executed!")

'''
    存储数据库至本地，以便之后使用
'''
def db_build():
    print("db_build() starting …")
    prepath = '/Users/lulu/Downloads/DuplicateChecking-master/docs'
    doc_name = os.listdir(prepath)
    global db_data, db_hash # 全局变量
    db_data = []
    db_hash = []
    count = 0
    for name in doc_name:
        # print(count, '\t', name)
        count += 1
        txt = np.loadtxt(codecs.open(os.path.join(prepath, name), encoding='utf-8',errors='ignore')
                        , dtype=np.str, delimiter="\n", encoding='utf-8')

        txtlist=list(map(lambda x:x.split("。"),np.array(list(txt))))
        txtarray=[]
        for item in txtlist:
            txtarray = np.append(txtarray,item)
        txtarray = np.char.replace(txtarray, u'\u3000',u'')
        for paragraph in txtarray:
            if paragraph == '' or paragraph == ' ' or paragraph.find(' ') != -1 or paragraph[0].isdigit():
                continue
            strKeyWord, shash = simhash(paragraph)
            if strKeyWord == '':
                continue
            db_data.append([name, paragraph, strKeyWord])
            db_hash.append(shash)
    print("db_build() executed!")

'''
    存储数据库至本地，以便之后使用
'''
def db_save():
    print("db_save() starting …")
    global db_data, db_hash  # 全局变量
    db_data = np.array(db_data)
    db_hash = np.array(db_hash)
    np.save("/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_data.npy", db_data)
    np.save("/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_hash.npy", db_hash)
    print("db_save() executed!")

'''
查重 - 准备工作
'''

from collections import OrderedDict
import numpy as np

def get_db_doc_idx(db_data):
    # print("get_db_doc_idx() starting …")
    global db_doc_idx  # 全局变量
    db_doc_idx = {}  # 初始化 db_doc_idx
    for i in range(len(db_data)): 
        arr = db_data[i]
        if arr[0] not in db_doc_idx.keys():
            db_doc_idx[arr[0]] = [i]
        else:
            db_doc_idx[arr[0]].append(i)
    # print("get_db_doc_idx() executed!")
    return db_doc_idx

def get_db_target_idx(db_data):
    # print("get_db_doc_idx() starting …")
    global db_target_idx  # 全局变量
    db_target_idx = {}  # 初始化 db_doc_idx
    for i in range(len(db_data)):
        arr = db_data[i]
        if arr[0] not in db_target_idx.keys():
            db_target_idx[arr[0]] = [i]
        else:
            db_target_idx[arr[0]].append(i)
    # print("get_db_doc_idx() executed!")
    return db_target_idx
# 单篇与数据库相似度（目标paper在数据库中）
def get_sim(paper_name, target_file,db_doc_idx, db_hash, hamming_dis_threshold=20):
    # print("get_sim() starting …")
    a_key = paper_name
    result_dict = {}
    print(db_data)
    for b_key in db_doc_idx.keys():

        if target_file != b_key:
            continue
        sim_count = 0
        for a_idx in db_doc_idx[a_key]:

            item = []
            for b_idx in db_doc_idx[b_key]:
                item_result = hammingDis(db_hash[a_idx], db_hash[b_idx])
                if item_result <= hamming_dis_threshold:
                    item.append([a_idx, b_idx])
            if len(item) > 0:
                sim_count += len(item)
        if sim_count > 0:
            result_dict[b_key] = sim_count
    
    result_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[1], reverse=True))
    
    # print("get_sim() executed!")
    return result_dict

# 单篇与数据库相似度（目标paper在不在数据库中）
def get_sim_notrain(paper_name, db_doc_idx, db_target_idx ,db_hash,db_target_hash, hamming_dis_threshold=5):
    # print("get_sim() starting …")
    a_key = paper_name
    result_dict = {}
    sim_count = 0
    print(db_doc_idx.keys())
    for a_idx in db_target_idx[a_key]:
            # print(a_key)
            item = []
            for b_idx in db_doc_idx[a_key]:

                item_result = hammingDis(db_target_hash[a_idx], db_hash[b_idx])

                if item_result <= hamming_dis_threshold:
                    item.append([a_idx, b_idx])
            if len(item) > 0:
               sim_count += len(item)
    if sim_count > 0:
        result_dict[b_idx] = sim_count
    result_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[1], reverse=True))
    print(result_dict)


    # for b_key in db_doc_idx.keys():
    #
    #     if a_key == b_key:
    #         continue
    #     sim_count = 0
    #     for a_idx in db_doc_idx[a_key]:
    #         print(a_key)
    #         print("a_idx")
    #         print(a_idx)#待测paper
    #         item = []
    #         for b_idx in db_doc_idx[b_key]:
    #             print("b_idx")
    #             print(b_idx)
    #             item_result = hammingDis(db_hash[a_idx], db_hash[b_idx])
    #             print(item_result)
    #             if item_result <= hamming_dis_threshold:
    #                 item.append([a_idx, b_idx])
    #         if len(item) > 0:
    #             sim_count += len(item)
    #     if sim_count > 0:
    #         result_dict[b_key] = sim_count

    result_dict = OrderedDict(sorted(result_dict.items(), key=lambda t: t[1], reverse=True))

    print("get_sim() executed!")
    return result_dict


# 两篇相似情况
def get_sim_details(paper_name_a, paper_name_b,  
                    db_doc_idx, db_hash, db_data, hamming_dis_threshold=200,
                    print_details='short'):
    # print("get_sim_details() starting …")
    a_key = paper_name_a
    b_key = paper_name_b
    result_dict = []
    similar_num=0
    print(db_doc_idx[paper_name_a])
    # txtlist=list(map(lambda x:nltk.text.Text(jieba.lcut(x[1])),db_data))
    txtlist=map(lambda x:nltk.text.Text(jieba.lcut(x[1])),db_data.tolist())
    fun_candidate = lambda x:nltk.text.Text(jieba.lcut(x[1]))
    fun_reference = lambda x:[nltk.text.Text(jieba.lcut(x[1]))]
    fun_score = lambda x,y:sentence_bleu(nltk.text.Text(jieba.lcut(x[1])), [nltk.text.Text(jieba.lcut(y[1]))],weights=(1, 0, 0, 0))
    append = lambda x,y:list.append({'b':x[1],'hamimng_distance':y})
    # print(db_data.tolist())
    print(txtlist)
    for a_idx in db_doc_idx[a_key]:
        list=[]
        candidate = fun_candidate(db_data[a_idx])
        for b_idx in db_doc_idx[b_key]:
            reference = fun_reference(db_data[b_idx][1])

            score = fun_score(db_data[b_idx], db_data[a_idx])
            print(score)
            if score > 0.5:
                print(db_data[b_idx][1])
                print(db_data[a_idx][1])
                print(score)
                append(db_data[b_idx],score)
                continue
            # item_sim = hammingDis(db_hash[a_idx], db_hash[b_idx])
            # if max_item_sim < item_sim:
            #     max_item_sim = item_sim
            # if item_sim <= hamming_dis_threshold:
            #     # if item_sim not in result_dict.keys():
            #     #     result_dict[item_sim] = []
            #     # result_dict[item_sim].append([db_data[a_idx], db_data[b_idx]])
            #     list.append({'b':db_data[b_idx][1],'hamimng_distance':item_sim})
                # addflag = 1

        result_dict.append({'a':db_data[a_idx][1],'list':list})
        # if addflag==0:
        #     result_dict.append({'a':db_data[a_idx][1],'b':"",'hamimng_distance':max_item_sim})
        # addflag=1
        # max_item_sim=0

    hamimng_distance  = similar_num/len(db_doc_idx[a_key])
    print("similar_num")
    print(similar_num)
    print(len(db_doc_idx[a_key]))
    # result_dict = OrderedDict(sorted(result_dict.items()))

    # print("get_sim_details() executed!")
    return result_dict,hamimng_distance

# 两篇相似情况
def get_sim_notrain_details(paper_name_a, paper_name_b,
                    db_doc_idx,db_hash, db_data, hamming_dis_threshold=5,
                    print_details='short'):
    print("get_sim_details() starting …")
    a_key = paper_name_a
    b_key = paper_name_b
    result_dict = {}
    print(db_target_data)
    for a_idx in db_target_idx[a_key]:
        for b_idx in db_doc_idx[b_key]:
            item_sim = hammingDis(db_target_hash[a_idx], db_hash[b_idx])
            if item_sim <= hamming_dis_threshold:
                if item_sim not in result_dict.keys():
                    result_dict[item_sim] = []
                result_dict[item_sim].append([db_target_data[a_idx], db_data[b_idx]])

    result_dict = OrderedDict(sorted(result_dict.items()))

    # full_path = GENERATE_PATH + '\\' + target_file
    # file = open(full_path, 'a')

    # if print_details == 'short':
        # print('paper a:', paper_name_a, '\npaper b:', paper_name_b, '\n', file=file)  # 打印标题
        # for k in result_dict.keys():
            # print('hamming distance:', str(k), file=file)
            # for a, b in result_dict[k]:
                # print('-'*100, file=file)
                # print('\ta:\t', a[1], file=file)
                # print('\tb:\t', b[1], file=file)
            # print('', file=file)

    # file = file.close()

    # print("get_sim_details() executed!")
    return result_dict

'''
     加载本地数据库
'''
def db_load():
    print("db_load() starting …")
    global db_data, db_hash ,db_target_data, db_target_hash# 全局变量

    db_data = np.load(r'/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_data.npy',encoding="latin1")
    db_hash = np.load(r'/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_hash.npy')
    # db_target_data = np.load(r'/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_target_data.npy',encoding="latin1")
    # db_target_hash = np.load(r'/Users/lulu/Downloads/DuplicateChecking-master/app/dupl_ckg/db_target_hash.npy')

    # print(db_target_data)
    # print(db_target_hash)

    print("db_load() executed!")

'''
    计算单篇与数据库中的相似度
    # 仅得数存在相似关系的的相关数据，值越大，越相似
'''
def result_sim(paper_name, GENERATE_PATH, target_file):
    print("result_sim() starting …")
    result_dict = get_sim(paper_name, target_file,db_doc_idx, db_hash, hamming_dis_threshold=10)
    print("result_sim() executed!")
    return result_dict

'''
    输出并打印两篇的相似情况
    # hamming distance 越小，越相似
'''
def result_details(paper_name_a, paper_name_b, GENERATE_PATH, target_file):
    print("result_details() starting …")
    
    global db_doc_idx  # 全局变量
    db_doc_idx = get_db_doc_idx(db_data)
    # print(db_doc_idx)
    result_dict_details,hamimng_distance = get_sim_details(paper_name_a, paper_name_b, db_doc_idx, db_hash, db_data, hamming_dis_threshold=10)
    

    # content = []
    # for k in result_dict_details.keys():
    #     item=[]
    #     for a, b in result_dict_details[k]:
    #         item.append({'a':a[1],'b':b[1]})
    #     content.append({'hamimng_distance':str(k),'item':item})
    json = {'audio_name': paper_name_a, 'book_name': paper_name_b, 'content': result_dict_details}
    json['hamimng_distance'] = hamimng_distance
    # print(json)

    print("result_details() executed!")
    return json


'''
    按相似度排序，打印相似段落
'''

def result_all(paper_name , target_file_name):
    db_load()
    print("result_details() starting …")
    
    # paper_name = '12.txt'
    global db_doc_idx ,db_target_idx# 全局变量
    db_doc_idx = get_db_doc_idx(db_data)

    # db_target_idx = get_db_target_idx(db_target_data)
    # print("11")
    # print(db_doc_idx)
    # result_dict = result_sim(paper_name, GENERATE_PATH, target_file_name)

    # print(GENERATE_PATH)
    # print(full_path)
    counter = 1
    # for paper_name_counter, hamming_dis in result_dict.items():
    #     json = result_details(paper_name, paper_name_counter, GENERATE_PATH, target_file_name)
    #     json['hamming_dis']=hamming_dis
    #
    #     counter += 1
    print("result_details() executed!")
    json = result_details(paper_name, target_file_name, GENERATE_PATH, target_file_name)

    print(json)
    return json
    
'''
    初始化数据库
'''

def init():
    print("init() starting …")
    db_build()  # 仅在库更新时再次 db_build() 和 db_save() 即可
    db_save()
    db_load()
    print("init() executed!")

# db_build()  # 仅在库更新时再次 db_build() 和 db_save() 即可
# db_target_build()
# db_build()
# db_save()
# db_load()
#
# # result_all('bailuyuan.txt', "110.txt")
# result_details("bailuyua1n.txt", "bailuyuan.txt", GENERATE_PATH,"111.txt")
# reference = [[u'我', u'真', u'的', u'很', u'爱', u'你']]
# candidate = [u'我', u'真', u'的', u'爱', u'你']
# score = sentence_bleu(reference, candidate,weights=(1, 0, 0, 0))
# print(score)
# reference = [['the', 'quick', 'brown','fox']]
# candidate = ['the', 'quick', 'brown', 'fox', 'jumped', 'over', 'the']

# reference = [['i', 'love', 'you']]
# candidate = ['i', 'love', 'you', 'too', 'but', 'i', 'do', 'not', 'love', 'he']
# score = sentence_bleu(reference, candidate,weights=(1, 0, 0, 0))
# print(score)
#
# candidate = ['i', 'love', 'you']
# reference = [['i', 'love', 'you', 'too', 'but', 'i', 'do', 'not', 'love', 'he']]
#
# score = sentence_bleu(reference, candidate,weights=(1, 0, 0, 0))
# print(score)
# print(score)
time_start=time.time()

# db_build()
# db_save()
result_all('白鹿原1右声道.txt', "白鹿原.txt")

time_end=time.time()
print('totally cost',time_end-time_start)
# result_details("白鹿原1右声道.txt", "白鹿原.txt", GENERATE_PATH,"111.txt")
