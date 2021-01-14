import os
import json
from pyhanlp import *
def is_chinese(strs):
    if len(strs) == 0:
        return False
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

def Update_Entity(cluster_path):
    f = open(cluster_path,"r",encoding='UTF-8')
    cluster_json = f.read()
    f.close()
    jdic = json.loads(cluster_json)
    doc_list = jdic['relate_article_list']
    data = ""
    for doc in doc_list:
        filepath = os.path.join(sentence_dir,doc[:10],doc+".fin")
        with open(filepath,"r",encoding="UTF8") as f:
            data += f.read()
        data += " "
    # get Entity
    n = set()
    tokens = HanLP.segment(data)
    for token in tokens:
        if str(token.nature)[0]=='n' and is_chinese(str(token.word)):
            n.add(token.word)
    # print(n)
    # Get TopK
    words = data.split(" ")
    dic_word = {}
    for word in words:
        if word not in dic_word:
            dic_word[word] = 0
        dic_word[word] += 1
    dic_word = sorted(dic_word.items(), key = lambda x:(x[1], x[0]),reverse=True)

    jdic["EntityTopK"] = []
    i = 0
    while i < len(dic_word):
        if dic_word[i][0] in n:
            jdic['EntityTopK'].append(dic_word[i][0])
        i += 1
        if len(jdic["EntityTopK"]) == 5:
            break
    print(jdic["EntityTopK"])
    orij = json.dumps(jdic,ensure_ascii=False)
    f = open(cluster_path,"w",encoding='UTF-8')
    f.write(orij)
    f.close()

if __name__=="__main__":
    L=input("L(2008-01):")
    R=input("R(2008-01):")

    Start = int(L.split("-")[1])
    End = int(R.split("-")[1])
    clu_dir = ".\\cluster"
    sentence_dir = ".\\tokens"
    for i in range(Start,End+1):# 按月更新
        if i < 10:
            mm = "0" + str(i)
        else :
            mm = str(i)
        dir = os.path.join(clu_dir,L.split("-")[0]+"-"+mm)
        if not os.path.isdir(dir):
            continue

        allfilelist = os.listdir(dir)
        for file in allfilelist:
            cluster_path = os.path.join(dir,file)
            Update_Entity(cluster_path)