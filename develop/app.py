# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, url_for
import json

app = Flask(__name__)  # 实例化app对象
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

ss = [
    {"event": "印尼海啸1", "num": "1", "abstract": "印尼爪哇岛南部印度洋海域当地时间17日下午3点20分左右发生强震，引发海啸。印尼官方称，海啸已造成668人死亡，当地缺乏预警系统。"},
    {"event": "印尼海啸2", "num": "2", "abstract": "印尼爪哇岛南部印度洋海域当地时间17日下午3点20分左右发生强震，引发海啸。印尼官方称，海啸已造成668人死亡，当地缺乏预警系统。"},
    {"event": "印尼海啸3", "num": "3", "abstract": "印尼爪哇岛南部印度洋海域当地时间17日下午3点20分左右发生强震，引发海啸。印尼官方称，海啸已造成668人死亡，当地缺乏预警系统。"},
    {"event": "印尼海啸4", "num": "4", "abstract": "印尼爪哇岛南部印度洋海域当地时间17日下午3点20分左右发生强震，引发海啸。印尼官方称，海啸已造成668人死亡，当地缺乏预警系统。"},
]

def get_event_list(search_val):
    cluster2event_filepath = 'static/data/cluster2event.json'
    file = open(cluster2event_filepath, "r", encoding="UTF-8")
    cluster2event_json = json.load(file)
    file.close()

    cluster_filepath_list = []
    event_name_list = []
    event_abstract_list = []
    for eventname in cluster2event_json:
        if search_val in eventname:
            cluster_filepath_list.append(cluster2event_json[eventname])
            event_name_list.append(eventname)
    # print(cluster_filepath_list)
    # print(event_name_list)
    ans = []
    for i in range(len(event_name_list)):
        event_name = event_name_list[i]
        file = open('static/data/' + cluster_filepath_list[i], "r", encoding="UTF-8")
        result_json = json.load(file)
        file.close()
        event_abstract = result_json["abstract"]
        tmp = {}
        tmp["event"] = event_name
        tmp["abstract"] = event_abstract
        tmp["starttime"] = result_json["start_time"]
        tmp["endtime"] = result_json["end_time"]
        t1 = float(result_json["emotion"]) * 100
        if t1 >= 70:
            tmp["face"] = "🙂"
            tmp["color"] = "color:#e00009"
        else:
            tmp["face"] = "🙁"
            tmp["color"] = "color:#67605f"
        ans.append(tmp)
    return ans
# selected_num = 0
year = ["2000", "2005", "2010"]

global_year = "2000"

# 尝试json
@app.route('/tryjson', methods=['GET', 'POST'])
def tryjson():
    x = request.args.get("value", "人类")
    return render_template('tryjson.html')

@app.route('/returnjson', methods=['GET', 'POST'])
def returnjson():
    event_name = request.args.get("value", "人类")
    print("data for kg json" + event_name)
    cluster2event_filepath = 'static/data/cluster2event.json'
    file = open(cluster2event_filepath, "r", encoding="UTF-8")
    cluster2event_json = json.load(file)
    file.close()

    result_cluster_filepath = 'cluster_0.json'
    for eventname in cluster2event_json:
        if event_name in eventname:
            result_cluster_filepath = cluster2event_json[event_name]
            break
    result_cluster_filepath = 'static/data/' + result_cluster_filepath
    file = open(result_cluster_filepath, "r", encoding="UTF-8")
    result_json = json.load(file)
    file.close()
    message_json = result_json["knowledge-data"]
    # message_json = {
    #     # name为key  不可重复
    #     "nodes": {
    #         "1": { "name": "特朗普", "type": "人物" },
    #         "2": { "name": "屎", "type": "物品" },
    #         "3": { "name": "卫生间", "type": "地点" },
    #         "4": { "name": "??", "type": "物品" },
    #         "5": { "name": "生间", "type": "地点" },
    #         "6": { "name": "asd屎", "type": "物品" }
    #     },
    #     "links": [ # type区分颜色，其他必须
    #         { "source": "1", "target": "2", "rela": "动作", "type": "吃了" },
    #         { "source": "1", "target": "3", "rela": "状语", "type": "位于" },
    #         { "source": "2", "target": "3", "rela": "状语", "type": "位于" },
    #         { "source": "2", "target": "4", "rela": "hah", "type": "于" }
    #     ]
    # }
    # print("ooo")
    return jsonify(message_json)

# 尝试ajax
@app.route('/more', methods=['GET', 'POST'])
def more():
    # print('fdsasdf')
    return 'sdafsadfsadfdsa'

@app.route('/sendjson', methods=['POST'])
def sendjson():
    # 接受前端发来的数据
    data = json.loads(request.form.get('data'))

    # lesson: "Operation System"
    # score: 100
    lesson = data["lesson"]
    score = data["score"]

    # 自己在本地组装成Json格式,用到了flask的jsonify方法
    info = dict()
    info['name'] = "pengshuang"
    info['lesson'] = lesson
    info['score'] = score
    print(info)
    return jsonify(info)

@app.route('/x', methods=['POST', 'GET'])
def xx():
    return render_template("x.html")

# 搜索事件后的搜索结果页面
@app.route('/search_result', methods=['POST', 'GET'])
def web():
    print("用户搜索")
    if request.method == 'POST':
        # th = request.form["op"]
        val = request.form["val"]
        print(val)
    elif request.method == 'GET':
        # th = request.args.get("op")
        val = request.args.get("val")
        print(val)
    search_val = request.args.get("value", "北京")
    print(search_val)
    # 检索事件，构造ss
    ss = get_event_list(search_val=search_val)
    return render_template("search_result.html", ss=ss, search_val=search_val)

# url_for,修改静态文件（js,css,image)时，网页同步修改
# @app.context_processor # 上下文渲染器，给所有html添加渲染参数
# def inject_url():
#   data = {
#     "url_for": dated_url_for,
#   }
#   return data
#
# def dated_url_for(endpoint, **values):
#     filename = None
#     if endpoint == 'static':
#         filename = values.get('filename', None)
#     if filename:
#         file_path = os.path.join(app.root_path, endpoint, filename)
#         values['v'] = int(os.stat(file_path).st_mtime) # 取文件最后修改时间的时间戳，文件不更新，则可用缓存
#     return url_for(endpoint, **values)

@app.route('/')
def hello_world():
    # return render_template('home_page.html', ss=ss, year=year, global_year=global_year)
    return render_template('main.html', ss=ss, year=year, global_year=global_year)

@app.route('/word-cloud')
def wc():
    pagenum = int(request.args.get("pagenum", "1"))
    if pagenum <= 0 or pagenum >= 9:
        return render_template('page_not_found.html')
    else:
        pass
    cur_year_list = []
    for cur_year in range((pagenum - 1) * 10 + 1946, pagenum * 10 + 1946):
        cur_year_list.append(str(cur_year))
    print(cur_year_list)
    pre_page_list = []
    next_page_list = []
    for x in range(1, pagenum):
        pre_page_list.append(str(x))
    for x in range(pagenum + 1, 9):
        next_page_list.append(str(x))
    return render_template('word-cloud.html', pagenum=pagenum, cur_year_list=cur_year_list, pre_page_list=pre_page_list, next_page_list=next_page_list)

@app.route('/about-us')
def au():
    return render_template('about-us.html')

@app.route('/uu')
def uu():
    return render_template('uu.html')

@app.route('/result/<num>')
def result(num):
    x = int(num)
    global  selected_num
    selected_num = num
    print(x)
    associate_event = []
    hot = None
    for s in ss:
        if s["num"] == num:
            hot = s
        else:
            associate_event.append(s)

    # 进入特定事件生成内容
    return render_template('result.html', associate_event=associate_event, hot=hot)

@app.route('/result1/<event_name>')
def result1(event_name):
    print(event_name)
    associate_event = []
    hot = None
    cluster2event_filepath = 'static/data/cluster2event.json'
    file = open(cluster2event_filepath, "r", encoding="UTF-8")
    cluster2event_json = json.load(file)
    file.close()

    result_cluster_filepath = 'cluster_0.json'
    for eventname in cluster2event_json:
        if event_name in eventname:
            result_cluster_filepath = cluster2event_json[event_name]
            break
    print("zzynb", result_cluster_filepath)

    result_cluster_filepath = 'static/data/' + result_cluster_filepath
    file = open(result_cluster_filepath, "r", encoding="UTF-8")
    result_json= json.load(file)
    file.close()
    hot = {}
    hot["event"] = event_name
    hot["abstract"] = result_json["abstract"]
    print(hot)
    keywords_list = result_json["keywords"]
    tmpset = set()
    for keyword in keywords_list[0:min(5, len(keywords_list))]:
        tmp = get_event_list(search_val=keyword)
        for x in tmp:
            if x['event'] == event_name:
                pass
            else:
                tmpset.add(x['event'])
    for keyword in keywords_list:
        tmp = get_event_list(search_val=keyword)
        for x in tmp:
            if x['event'] in tmpset:
                tmpset.remove(x['event'])
                associate_event.append(x)
    print("dssfasdfdsafdsaf")
    print(associate_event)
    emotion_value = float(result_json["emotion"]) * 100
    # 进入特定事件生成内容
    # emotion_value = "0.8"
    print("--------------------")
    origin_dict = result_json["timeline"]
    print(origin_dict)
    xlist = []
    timelist = []
    for timex in origin_dict:
        stime = timex.split('-')
        timelist.append(stime[1] + '-' + stime[2])
        # timelist.append((timex))
        xlist.append(int(origin_dict[timex]))
    print(xlist)
    print(timelist)
    # date_dict = {
    #     20080807:0,
    #     20080808:0,
    #     20080809:0
    # }
    article_list_s = result_json["relate_article_list"]
    # for article in article_list_s:
    #     s_list = article.split('-')
    #     ss = s_list[0] + s_list[1] + s_list[2]
    #     datex = int(ss)
    #     date_dict[datex] = date_dict[datex] + 1
    # for datex in range(20080807, 20080810):
    #     xlist.append(date_dict[datex])
    return render_template('result1.html', associate_event=associate_event, hot=hot, emotion_value=emotion_value, xlist=xlist, timelist=timelist)

@app.route('/lrz')
def lrz():
    # return render_template('home_page.html', ss=ss, year=year, global_year=global_year)
    return render_template('lrz.html')


@app.route('/sendlrz', methods=['GET', 'POST'])
def sendlrz():
    # 接受前端发来的数据
    data = json.loads(request.form['cur_year'])
    print(data)
    cur_year = data
    # lesson: "Operation System"
    # score: 100
    # lesson = data["lesson"]
    # score = data["score"]

    # 自己在本地组装成Json格式,用到了flask的jsonify方法
    info = dict()
    info['奥运'] = 100 + cur_year - 1946
    info['北京'] = 80 + cur_year - 1946
    info['开心'] = 75 + cur_year - 1946

    # info['name'] = "pengshuang"
    # info['lesson'] = lesson
    # info['score'] = score
    print(info)
    return jsonify(info)

@app.route('/ajaxlrz', methods=['GET', 'POST'])
def ajaxlrz():
    # 接受前端发来的数据
    data = json.loads(request.form.get('data'))
    print(data)
    cur_year = data["cur_year"]
    # lesson: "Operation System"
    # score: 100
    # lesson = data["lesson"]
    # score = data["score"]

    # 自己在本地组装成Json格式,用到了flask的jsonify方法
    info = dict()
    info['word_list'] = ['奥运', '北京', '开心']
    info['frequency_list'] = [100 + cur_year - 1946, 80 + cur_year - 1946, 75 + cur_year - 1946]

    filepath = 'static/data/top10words.json'
    file = open(filepath, "r", encoding="UTF-8")
    all_info = json.load(file)
    file.close()
    print(type(all_info))
    if str(cur_year) in all_info:
        info = all_info[str(cur_year)]

    print(info)
    return jsonify(info)

@app.route('/hot-words')
def hot_words():
    # return render_template('home_page.html', ss=ss, year=year, global_year=global_year)
    return render_template('hot-words.html')

@app.route('/water')
def water():
    # return render_template('home_page.html', ss=ss, year=year, global_year=global_year)
    return render_template('water.html')
