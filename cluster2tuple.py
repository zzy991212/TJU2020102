from getdate import *
from pyhanlp import *
import json
import os

def is_chinese(strs):
    if len(strs) == 0:
        return False
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True


def get_3_tuple(data):
    ans_t1 = []
    ans_att = []
    for d in data:
#         print(d)
        x = HanLP.parseDependency(d)
        wordArr = x.getWordArray()
        dic = {}
        main_v = ""
        for ids in range(len(wordArr)):
            if wordArr[ids].HEAD.LEMMA not in dic:
                dic[wordArr[ids].HEAD.LEMMA] = {}
            if wordArr[ids].LEMMA not in dic:
                dic[wordArr[ids].LEMMA] = {}
            dic[wordArr[ids].HEAD.LEMMA][wordArr[ids].DEPREL] = wordArr[ids].LEMMA
            if wordArr[ids].HEAD == Jv.ROOT:
                main_v = wordArr[ids].LEMMA

        if main_v not in dic:
            continue
        # 根据句子进行提取关系
        sub = []
        ver = []
        
        if '主谓关系' in dic[main_v]: # 提取所有主语
            now_sub = dic[main_v]['主谓关系']
            sub.append(now_sub)
            while '并列关系' in dic[now_sub]:
                now_sub = dic[now_sub]['并列关系']
                if now_sub in sub:
                    break
                sub.append(now_sub)
                
        now_ver = main_v
        ver.append(now_ver)
        while '并列关系' in dic[now_ver]: # 提取并列动词
            obj = []
            if '动宾关系' in dic[now_ver]: # 提取该动词宾语
                now_obj = dic[now_ver]['动宾关系']
                obj.append(now_obj)
                while '并列关系' in dic[now_obj]:
                    now_obj = dic[now_obj]['并列关系']
                    if now_obj in obj:
                        break
                    obj.append(now_obj)
            for x1 in sub:
                for x3 in obj:
                    if [x1,now_ver,x3] not in ans_t1:
                        ans_t1.append([x1,now_ver,x3,d])
                        
            now_ver = dic[now_ver]['并列关系']
            if now_ver in ver:
                break
            ver.append(now_ver)
            
        obj = []
        if '动宾关系' in dic[now_ver]: # 提取最后一个并列动词的宾语
            now_obj = dic[now_ver]['动宾关系']
            obj.append(now_obj)
            while '并列关系' in dic[now_obj]:
                now_obj = dic[now_obj]['并列关系']
                if now_obj in obj:
                    break
                obj.append(now_obj)
            for x1 in sub:
                for x3 in obj:
                    if [x1,now_ver,x3] not in ans_t1:
                        ans_t1.append([x1,now_ver,x3,d])
#         print(d)
        for item in wordArr:
            if item.DEPREL == '定中关系':
#                 print([item.LEMMA,"修饰",item.HEAD.LEMMA])
                    ans_att.append([item.LEMMA,"修饰",item.HEAD.LEMMA,d])
    return ans_t1,ans_att

def find_3_tuple(cluster_path):
    f = open(cluster_path,"r",encoding='UTF-8')
    cluster_json = f.read()
    f.close()
    jdic = json.loads(cluster_json)
    doc_list = jdic['relate_article_list']
    data = ""
    f = open(sentence_dir+"\\"+doc_list[0][:-5]+"\\"+doc_list[0]+".sen","r",encoding='UTF-8')
    data = f.read()
    whole_data = data
    data = data.split(" ")
    clu_t1,clu_att = get_3_tuple(data)
    clu_keywords = jdic['keywords']
    final_t = []
    final_att = []
    for tup in clu_t1:
        cnt = 0
        if tup[0] in clu_keywords:
            cnt += 1
        if tup[1] in clu_keywords:
            cnt += 1
        if tup[2] in clu_keywords:
            cnt += 1
        if cnt >= 2:
            final_t.append(tup)
    for tup in clu_att:
        if tup[0] in clu_keywords or tup[2] in clu_keywords:
            final_att.append(tup)
    result = ""
    if len(final_t) != 0:
        # print(final_t[0])
        topic_sentence = final_t[0]

        sentence = topic_sentence[3]
        tmp = HanLP.parseDependency(sentence)
        wordArr = tmp.getWordArray()
        dic = {}
        main_v = ""
        for ids in range(len(wordArr)):
            if wordArr[ids].HEAD.LEMMA not in dic:
                dic[wordArr[ids].HEAD.LEMMA] = {}
            if wordArr[ids].LEMMA not in dic:
                dic[wordArr[ids].LEMMA] = {}
            if wordArr[ids].DEPREL not in dic[wordArr[ids].HEAD.LEMMA]:
                dic[wordArr[ids].HEAD.LEMMA][wordArr[ids].DEPREL] = []
            dic[wordArr[ids].HEAD.LEMMA][wordArr[ids].DEPREL].append(wordArr[ids].LEMMA)
            if wordArr[ids].HEAD == Jv.ROOT:
                main_v = wordArr[ids].LEMMA 
        main_v = topic_sentence[1]
        now = 0
        # print(main_v)
        sub = topic_sentence[0]
        obj = topic_sentence[2]
        now = [sub]
        find_att(sub,now,dic)
        for i in range(len(now)):
            result += now[len(now)-i-1]

        result += main_v
        now = [obj]

        find_att(obj,now,dic)

        if "主谓关系" in dic[obj]:
            result += dic[obj]["主谓关系"][0]

        for i in range(len(now)):
            result += now[len(now)-i-1]

        if "动宾关系" in dic[obj]:
            result += dic[obj]["动宾关系"][0]

    jdic['topic'] = result
    jdic['abstract'] = HanLP.getSummary(whole_data,100)
    # zhaiyao = [] 
    
    # for abst in final_t:
    #     if abst[3] not in zhaiyao:
    #         zhaiyao.append(abst[3])
    #         jdic['abstract'] += abst[3]
    
    node_mp = set()
    for tup in final_t:
        node_mp.add(tup[0])
        node_mp.add(tup[2])
    for tup in final_att:
        node_mp.add(tup[0])
        node_mp.add(tup[2])

    jdic["knowledge-data"] = {}
    node_dic = {}
    node_d = {}
    cnt = 0
    for x in node_mp:
        cnt += 1
        node_d[x] = str(cnt)
        node_dic[str(cnt)]={"name":x,"type":str(HanLP.segment(x)[0].nature)}
    jdic["knowledge-data"]["nodes"] = node_dic

    link_list = []
    for tup in final_t:
        if {"source": node_d[tup[0]], "target": node_d[tup[2]], "rela": tup[1], "type": "svo"} not in link_list:
            link_list.append({"source": node_d[tup[0]], "target": node_d[tup[2]], "rela": tup[1], "type": "svo"})
    for tup in final_att:
        if {"source": node_d[tup[0]], "target": node_d[tup[2]], "rela": tup[1], "type": "att"} not in link_list:
            link_list.append({"source": node_d[tup[0]], "target": node_d[tup[2]], "rela": tup[1], "type": "att"})
    jdic["knowledge-data"]["links"]=link_list

    orij = json.dumps(jdic,ensure_ascii=False)
    f = open(cluster_path,"w",encoding='UTF-8')
    f.write(orij)
    f.close()
    print(jdic["cluster_id"])

def find_att(x,now,dic):
    if x in now:
        return
    while "定中关系" in dic[x]:
        for i in range(len(dic[x]['定中关系'])):
            now.append(dic[x]['定中关系'][len(dic[x]['定中关系'])-i-1])
            find_att(dic[x]['定中关系'][len(dic[x]['定中关系'])-i-1],now,dic)
            

if __name__=="__main__":
    L=int(input("L_year:"))
    R=int(input("R_year:"))
    clu_dir = "./cluster"
    sentence_dir = "./tokens"
    Jv = JClass("com.hankcs.hanlp.corpus.dependency.CoNll.CoNLLWord")
    for i in range(L,R+1):# 按年找热点事件
        dir = clu_dir+"/"+str(i)
        if not os.path.isdir(dir):
            continue

        allfilelist = os.listdir(dir)
        for file in allfilelist:
            cluster_path = os.path.join(dir,file)
            find_3_tuple(cluster_path)
