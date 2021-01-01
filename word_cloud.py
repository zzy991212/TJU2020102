import wordcloud
import matplotlib.pyplot as plt
import jieba
import os
import numpy as np
import imageio
import jieba.posseg as pseg
from matplotlib import colors

def get_file_list(dir,L,R):    
    global text
    allfilelist = os.listdir(dir)
    for file in allfilelist:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):
            now_year = int(filepath.split("-")[0][-4:])
            if now_year >= L and now_year <= R:
                get_file_list(filepath,L,R)
        elif os.path.isfile(filepath):
            if filepath[-3:] == 'fin':
                f = open(filepath,"r",encoding="utf8")
                data = f.read()
                text += data
                f.close()


L = int(input("L:"))
R = int(input("R:"))
for i in range(L,R+1):
    text = ""
    mk=imageio.imread("./img/"+str(i)+".png")
    color_list=['#F5FFFA',"#FFFFE0",'#FAFAD2','#FFFACD','#FDF5E6',"#F5DEB3","#FAF0E6","#FFF5EE","#FFEFD5","#FDF5E6"]#建立颜色数组
    colormap=colors.ListedColormap(color_list)#调用
    w = wordcloud.WordCloud(scale=5,font_path='simhei.ttf', background_color=None,colormap=colormap,mode='RGBA', mask=mk,max_words=500,relative_scaling=0.7)
    get_file_list('./'+'tokens',i,i)
    words = text.split(" ")
    dic_word = {}
    for word in words:
        tags = pseg.lcut(word)
        if len(tags) == 0:
            continue
        tag = tags[0]
        if tag.flag == 'x' or tag.flag == 'm' or tag.flag == 'r' or tag.flag == 'f':
            continue
        else:
            if tag.word not in dic_word:
                dic_word[tag.word] = 0
            dic_word[tag.word] += 1
    w.generate_from_frequencies(dic_word)
    print(str(i)+"词云生成")
    w.to_file('./wordcloud/'+str(i)+".png")
