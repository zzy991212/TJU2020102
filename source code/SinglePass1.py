from pyhanlp import HanLP
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import os
from gensim.models import Word2Vec
import numpy as np
from getdate import *
import json
# f = open("..\\test_clean_data\\rmrb\\1946-05-15\\1946-05-15-0000.fin","r",encoding='UTF-8')
# data = f.read()
# print(data)

def is_chinese(strs):
    if len(strs) == 0:
        return False
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

class Article(): # 文本类
    def __init__(self,doc_id,feature,content):
        self.doc_id = doc_id # 存放文本序号（文件名）
        self.feature = feature # 特征值
        self.content = content # 分词后的文本

class Cluster(): # 聚类
    def __init__(self,cluster_id,center_doc_id):
        self.cluster_id = cluster_id # 簇序号
        self.center_doc_id = center_doc_id # 中心文档编号
        self.member = [center_doc_id] # 簇成员列表

    def add_doc(self,doc_id):
        self.member.append(doc_id)

class SinglePass_v1():
    def __init__(self):
        self.doc_map = {} # Key: doc_id, Value: Article()
        self.clu_map = {}
        self.clu_iid = {}

    def process(self,docs):
        self.prepare(docs)
        self.clustering()
    
    def tfidf_cal(self,docs,docs_content,K=25):
        def cut(sentence):
            return sentence.split(" ")
        #TF-IDF
        vectorizer = CountVectorizer(analyzer="word", tokenizer=cut)  # 将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i个文本下的词频
        transformer = TfidfTransformer()  # 统计每个词语的tf-idf权值
        X = vectorizer.fit_transform(docs_content)
        tfidf = transformer.fit_transform(X)  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
        word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
        weight = tfidf.toarray() # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i个文本中的tf-idf权重
        # Top K
        for i in range(len(weight)):  # 每个文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一个文本下的词语权重
            word_tfidf = {}
            for j in range(len(word)):
                if weight[i][j] != 0:
                    word_tfidf[word[j]] = weight[i][j]
            doc_feature = sorted(word_tfidf.items(), key=lambda x: x[1],reverse=True)[:K]
            doc_feature = list(map(lambda x: x[0], doc_feature))
            final_feature = []
            cnt = 0
            for x in doc_feature:
                if is_chinese(x):
                    final_feature.append(x)
                    cnt += 1
                if cnt>K-5:
                    break
            article = Article(docs[i][0],final_feature,docs[i][1])
            self.doc_map[docs[i][0]] = article

    
    def prepare(self,docs):# 预处理：提取特征并转化成向量
        docs_content = []
        for article in docs:
            docs_content.append(article[1])

        self.tfidf_cal(docs,docs_content)
            # print(docs[i][0] + str(doc_feature))

    def clustering(self):
        for doc_id in self.doc_map:
            doc_feature = self.doc_map[doc_id].feature
            flag = True
            for cluster_id in self.get_cand_clusters(doc_feature):
                cluster = self.clu_map[cluster_id]
                if self.similar(cluster,self.doc_map[doc_id]):
                    cluster.add_doc(doc_id)
                    flag = False
                    break
            if flag:
                new_clu_id = "cluster_" + str(len(self.clu_map))
                print("Constract new "+new_clu_id)
                new_cluster = Cluster(new_clu_id,doc_id)
                self.clu_map[new_clu_id] = new_cluster

                for word in self.doc_map[new_cluster.center_doc_id].feature:
                    if word not in self.clu_iid:
                        self.clu_iid[word] = []
                    self.clu_iid[word].append(new_clu_id) 
                
    def get_cand_clusters(self,feature):
        cand_cluster_id = []
        for word in feature:
            cand_cluster_id.extend(self.clu_iid.get(word,[]))
        return cand_cluster_id

    def similar(self,cluster,article):
        clu_feature = list(set(self.doc_map[cluster.center_doc_id].feature))
        doc_feature = list(set(article.feature))
        Total_si = 0
        vis = np.zeros(len(clu_feature))
        for word in doc_feature:
            mxs = 0
            pl = -1
            for i in range(len(clu_feature)):
                if not vis[i]:
                    if word in model and clu_feature[i] in model:
                        si = model.wv.similarity(word,clu_feature[i])
                        if si > mxs:
                            mxs = si
                            pl = i
            if mxs > 0.83 and pl != -1:
                Total_si += 1
                vis[pl] = 1
        if Total_si >= 8:
            return True
        else:
            return False

        # OLD: USING SET
        #
        # similarity_v = len(clu_feature & doc_feature) / len(clu_feature | doc_feature)
        # # print(cluster.center_doc_id + " " + article.doc_id + " v=" + str(similarity_v))
        # if similarity_v >= 0.14:
        #     return True
        # else:
        #     return False
    
    def show_result(self,K=25):
        for cluster_id in self.clu_map:
            cluster = self.clu_map[cluster_id]
            keyword_mp = {}
            for doc_id in cluster.member:
                for word in self.doc_map[doc_id].content.split(' '):
                    if word not in self.doc_map[doc_id].feature:
                        continue
                    if word not in keyword_mp:
                        keyword_mp[word] = 0
                    keyword_mp[word] += 1
            keyword = sorted(keyword_mp.items(), key=lambda x: x[1],reverse=True)[:K]
            keyword = list(map(lambda x: x[0], keyword))
            final_keyword = []
            cnt = 0
            for x in keyword:
                if is_chinese(x):
                    final_keyword.append(x)
                    cnt += 1
                if cnt>K-5:
                    break
            self.save_as_json(cluster,final_keyword)
            print(cluster.cluster_id,"members:",cluster.member," keywords: ",final_keyword)
    
    def save_as_json(self,cluster,keyword):
        filepath = "./cluster"
        center_id = cluster.center_doc_id
        year_id = center_id.split("-")[0]
        if not os.path.exists(filepath+"/"+year_id):
            os.mkdir(filepath+"/"+year_id)
        filepath = filepath+"/"+year_id
        dic = {}
        dic["cluster_id"] = cluster.cluster_id
        dic["topic"] = ""
        dic["abstract"] = ""
        dic["relate_article_list"] = cluster.member
        dic["keywords"] = keyword
        json_dic = json.dumps(dic,ensure_ascii=False)
        f = open(filepath+"/"+cluster.cluster_id+".json","w",encoding="utf8")
        f.write(json_dic)
        f.close()

def get_file_list(dir):    
    allfilelist = os.listdir(dir)
    for file in allfilelist:
        filepath = os.path.join(dir,file)
        if os.path.isfile(filepath):
            if filepath[-3:] == 'fin':
                f = open(filepath,"r",encoding="utf8")
                data = f.read()
                doc_id = filepath.split(".")[0][-15:]
                # print(doc_id)
                docs.append([doc_id,data])
                f.close()

if __name__ == '__main__':
    model = Word2Vec.load("./word2vec_model/2008.model")
    docs = []
    L=input("L:(eg:1946-05-15)")
    R=input("R:(eg:1946-05-15)")
    datelist = get_date_list(L,R)
    for date in datelist:
        get_file_list('./'+'tokens/'+date)
    single_passor = SinglePass_v1()
    single_passor.process(docs)
    single_passor.show_result()


    