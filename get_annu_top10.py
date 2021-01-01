import wordcloud
import matplotlib.pyplot as plt
import jieba
import os
import numpy as np
import imageio
import jieba.posseg as pseg
from matplotlib import colors
import json

def get_file_list(dir):
    # print(dir)
    global text
    allfilelist = os.listdir(dir)
    for file in allfilelist:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):
            get_file_list(filepath)
        elif os.path.isfile(filepath):
            if filepath[-3:] == 'fin':
                lists.append(filepath)
                # f = open(filepath,"r",encoding="utf8")
                # data = f.read()
                # text += data
                # f.close()


L = int(input("L:"))
R = int(input("R:"))
lists = []
get_file_list('./'+'tokens')
print("---Finish read file list!------")
f = open("./top10words.json","r",encoding='UTF-8')
ori_json = f.read()
f.close()
js = json.loads(ori_json)
for i in range(L,R+1):
    text = ""
    for x in lists:
        if x[-19:][:4] == str(i):
            f = open(x,"r",encoding="utf8")
            data = f.read()
            text += data
            f.close()

    words = text.split(" ")
    dic_word = {}
    for word in words:
        if word not in dic_word:
            dic_word[word] = 0
        dic_word[word] += 1
    dic_word = sorted(dic_word.items(), key = lambda x:(x[1], x[0]),reverse=True)

    cnt = 0
    ans = {}
    ans["word_list"] = []
    ans["frequency_list"] = []
    for x in dic_word:
        tags = pseg.lcut(x[0])
        if len(tags) == 0:
            continue
        tag = tags[0]
        # if tag.flag == 'x' or tag.flag == 'm' or tag.flag == 'r' or tag.flag == 'f':
        #     continue
        if tag.flag[0] == 'n' and len(x[0]) > 1:
            ans["word"].append(x[0])
            ans["frequency"].append(x[1])
            cnt += 1
            if cnt >= 10:
                break
    js[str(i)] = ans
    print(i)
    print(ans)
    print("---------------------------")
    final_json = json.dumps(js,ensure_ascii=False)
    f = open("./top10words.json","w",encoding='UTF-8')
    f.write(final_json)
    f.close()


