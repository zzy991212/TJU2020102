

# TJU2020102小组代码仓库

## 后端算法文件夹树如下（在仓库中暂未给出部分文件夹内容）

----rmrb
    |----XXXX-XX-XX(年-月-日)
    |    |----XXXX-XX-XX-XXXX.txt(年月日序号)
----cluster
    |----XXXX(年)
    |----|----cluster_X.json(X为序号)
----img
    |----XXXX.png(以年份命名的词云背景图)
----stopwords-master(存放停等词)
    |----略
----cleancode(yxn写的部分，会被引用，无需修改)
    |----\_\_init\_\_.py
    |----basic_mod.py
    |----cleaning.py
    |----config.py
----tokens(存放分句、分词后的文本)
    |----XXXX-XX-XX(年-月-日)
    |    |----XXXX-XX-XX-XXXX.cle(初步清洗)
    |    |----XXXX-XX-XX-XXXX.fin(分词后的内容)
    |    |----XXXX-XX-XX-XXXX.sen(句子用空格隔开)
----word2vec_model(存放word2vec模型)
    |----略
----wordcloud(存放词云)
    |----XXXX.png(以年份命名的词云)
simhei.ttf(字体文件，用来生成词云)
getdate.py(会被引用，无需修改)
tokens.py(第1步，分句分词，输入为年份区间)
word_cloud.py(第2步，生成词云，输入年份区间，需要确保img里有对应年份的背景图)
word_vec.py(第3步，预训练word2vec模型，其中注释部分为输入区间然后生成文件并保存，其他部分为测试加载模型是否成功)
SinglePass1.py(第4步，读取模型，输入日期区间，生成聚类)
cluster2tuple.py(第5步，将cluster读取出来并生成三元组、事件名称、时间摘要)