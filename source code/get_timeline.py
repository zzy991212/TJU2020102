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

# print(sen_dic)
import datetime
def get_date_list(start,end):
    date_list= []
    date = datetime.datetime.strptime(start,'%Y-%m-%d')
    end = datetime.datetime.strptime(end,'%Y-%m-%d')
    while date <= end:
        date_list.append(date.strftime('%Y-%m-%d'))
        date = date + datetime.timedelta(1)
    return date_list

filepath = "./cluster/lhmnb"

text = []
get_file_list(filepath)

for file in text:
    with open(file,"r",encoding="UTF-8") as f:
        clu = json.loads(f.read())
    timeline = {}
    arti = clu["relate_article_list"]
    clu["start_time"] = arti[0][0:10]
    clu["end_time"] = arti[len(arti)-1][0:10]
    starts = "2008-08-01"
    ends = "2008-08-31"
    date_list = get_date_list(starts,ends)
    for date in date_list:
        timeline[date] = '0'
    for ar_id in arti:
        timeline[ar_id[0:10]] = str(eval(timeline[ar_id[0:10]]+"+1"))
    clu["timeline"] = timeline
    with open(file,'w',encoding="UTF-8") as f:
        f.write(json.dumps(clu,ensure_ascii=False))

