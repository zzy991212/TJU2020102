import os
import re
import sys
import copy
import codecs
import jieba
import datetime
import json
from aip import AipNlp
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

MAX_LEN = 100


def load_stopword():
    f_stop = open('stopwords.txt', encoding='utf-8')  # 中文停用词表
    sw = [line.strip() for line in f_stop]  # strip() 方法用于移除字符串头尾指定的字符（默认为空格）
    f_stop.close()
    return sw


def getConceptAndTarget(cluster, kid):
    keyw = cluster["keywords"][kid]
    concept = [keyw]
    target = []
    model = Word2Vec.load('./word2vec_model/2008.model')
    words = model.wv.index2word   
    for key in model.wv.similar_by_word(keyw, topn = 10):
        target.append(key[0])
    return concept, target


def is_chinese(strs):
    if len(strs) == 0:
        return False
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def getSentimentScore(sen):
    APP_ID = '10987797'
    API_KEY = 'cgZ7P9szshd6UcTaQIzOvugS'
    SECRET_KEY = 'xUXD6DYFmYpDwMfXpTkVciWWdBYPX8ZE'
    client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
    client.setConnectionTimeoutInMillis(200)
    client.setSocketTimeoutInMillis(200)
    
    sentiment_category = {2:1.0, 0:-1.0, 1:0.0}

    s = client.sentimentClassify(sen)
    sentiment_score = 0.0

    if 'items' not in s.keys():
        sentiment_score = 0.0
    else:
        sentiment = sentiment_category[s['items'][0]['sentiment']]
        confidence = s['items'][0]['confidence']
        sentiment_score = sentiment*confidence
    # print("got ", sentiment_score)
    return sentiment_score


def getScore(cluster, kid):
    stopwords = load_stopword()
    concept, target = getConceptAndTarget(cluster, kid)
    scores_c = []
    scores_t = []
    cstring = ""
    tstring = ""
    lc = 0
    lt = 0
    for di in cluster["relate_article_list"]:
        with codecs.open("./data/"+di+".sen",'r','utf-8') as f:
            lines = f.read().split(" ")
            for line in lines:
                line = line.strip()
                data_token = jieba.lcut(line)
                words = []
                for word in data_token:
                    if word not in stopwords:
                        if is_chinese(word):
                            words.append(word)
                words = set(words)
                wc = len(words & set(concept)) 
                wt = len(words & set(target))

                if wc != 0:
                    if lc + len(line) > MAX_LEN:
                        score = getSentimentScore(cstring)
                        scores_c.append(score)
                        lc = len(line)
                        cstring = line + " "
                    else:
                        lc += len(line)
                        cstring += line + " "
                if wt != 0:
                    if lt + len(line) > MAX_LEN:
                        score = getSentimentScore(tstring)
                        scores_t.append(score)
                        lt = len(line)
                        tstring = line + " "
                    else:
                        lt += len(line)
                        tstring += line + " "
    score = getSentimentScore(cstring)
    scores_c.append(score)
    score = getSentimentScore(tstring)
    scores_t.append(score)
    return scores_c, scores_t

def getEI(cluster_name):
    path = './cluster/'
    with open(path + cluster_name + '.json','r',encoding='utf8') as f:
        cluster = json.loads(f.read())
        for kid in range(min(5,len(cluster["keywords"]))):
            print(kid)
            scores_c, scores_t = getScore(cluster, kid)
            # 防止除0，+1
            explicit_attitude = sum(scores_c) / (len(scores_c)+1)
            implicit_attitude = sum(scores_t) / (len(scores_t)+1)
            if kid == 0:
                dic[cluster_name] = {}
            dic[cluster_name][cluster["keywords"][kid]] = {'ex': explicit_attitude,'im': implicit_attitude}
            # print("外显情感: ", explicit_attitude, "\n内隐情感: ", implicit_attitude)
        # return explicit_attitude, implicit_attitude

if __name__ == "__main__":
    dic = {}
    for ii in range(1149):
        getEI('cluster_'+str(ii))
        print(str(ii) + ' ok!')
        json_str = json.dumps(dic)
        with open('emo_ex_im.json', 'w') as json_file:
            json_file.write(json_str)

