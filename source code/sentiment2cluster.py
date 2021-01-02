import json
import os
def get_file_list(dir):    
    global text
    allfilelist = os.listdir(dir)
    for file in allfilelist:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):
            get_file_list(filepath)
        elif os.path.isfile(filepath):
            text.append(filepath)

with open("Sentiment.json","r",encoding="UTF-8") as f:
    sen_dic = json.loads(f.read())
# print(sen_dic)

filepath = "./cluster/2008"

text = []
get_file_list(filepath)

for file in text:
    with open(file,"r",encoding="UTF-8") as f:
        clu = json.loads(f.read())
    main_id = clu['relate_article_list'][0]
    clu['emotion'] = sen_dic[main_id]
    with open(file,'w',encoding="UTF-8") as f:
        f.write(json.dumps(clu,ensure_ascii=False))

