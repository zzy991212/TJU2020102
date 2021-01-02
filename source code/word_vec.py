from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import jieba
from zhon.hanzi import punctuation
import re
import os
sentences = []

def get_file_list(dir,L,R):    
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
                sentences.append(data.split(" "))
                f.close()

L = int(input("L:"))
R = int(input("R:"))
get_file_list('./'+'tokens',L,R)
model = Word2Vec(sentences, size = 150, window=7, min_count=1,iter=8)
model.save('./word2vec_model/'+str(L)+'.model')
# model = Word2Vec.load('.\\word2vec_model\\2008.model')

# words = model.wv.index2word
# print(words)    
# for key in model.wv.similar_by_word("奥运会", topn =100):
#     print(key)

# print(model["学习"])
# for key in model.wv.similar_by_word('机器学习', topn =3):
#     print(key)
# wv =model.wv.vocab.keys()
# print(wv)