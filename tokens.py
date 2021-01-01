import sys
import cleancode.cleaning as cle
import cleancode.basic_mod as bm
import re
from zhon.hanzi import punctuation
import jieba.posseg as pseg
import jieba
from cleancode.config import *

def load_stopword():
    f_stop = open('./stopwords-master/baidu_stopwords.txt', encoding='utf-8')  # 中文停用词表
    sw = [line.strip() for line in f_stop]  # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    f_stop.close()
    return sw

def tokens(filename):
    f = open(filename,"r",encoding='UTF-8')
    data = f.read()

    #replace chinese num,delete punctuation
    pattern = re.compile(r'[\uff10-\uff19]')
    for i in range(len(data)):
        ifcnum = re.search(pattern,data[i])
        if ifcnum:
            uni = data[i].encode('unicode_escape').decode('utf-8')
            data = data.replace(data[i],uni[-1])
    # data = re.sub("[{}]".format(punctuation)," ",data)
    data = re.sub(r'[”。？！：；“×]',"。 ",data)

    x = open(filename[:-3]+'sen',"w",encoding='UTF-8')
    x.write(data)
    x.close()  

    data = re.sub("[{}]".format(punctuation)," ",data)
    # delete stopwords
    data_token = jieba.lcut(data)
    stopwords = load_stopword()
    out_str = ""
    for word in data_token:
        if word not in stopwords:
            if word != '\t':
                out_str += word
        out_str += " "
    
    out_str = re.sub(r' +', " ", out_str)
    out_str = re.sub(r'　+', " ", out_str)
    # print(out_str)

    x = open(filename[:-3]+'fin',"w",encoding='UTF-8')
    x.write(out_str)
    x.close()    
    # tagging
    tags = pseg.lcut(out_str)
    # print(tags)

def select(filelist):
    for filename in filelist:
        if filename[-3:] == 'cle':
            tokens(filename)

# clean
L = int(input("Start year:"))
R = int(input("End year:"))
# cle.cleaning(L,R)
filelist = bm.get_file_list('./'+'tokens',L,R)
select(filelist)

