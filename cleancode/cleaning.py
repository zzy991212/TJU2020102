import re

from .basic_mod import get_file_list
from .config import *
import time
import os

def confir(line):
    for i in range(0,32):
        line = line.replace(chr(i),'')
    line = re.sub(r'第[0-9]*版\(.*\)专栏：', "", line)
    line = re.sub(r'.*讯　', "", line)
    line = re.sub(r'.*电　', "", line)
    line = re.sub(r'.*讯 ', "", line)
    line = re.sub(r'.*电 ', "", line)
    line = re.sub(r'【[^】【]*】', "", line)
    line = re.sub(r'（[^（）]*）', "", line)
    line = re.sub(r'\([^\(\)]*\)', "", line)
    line = re.sub(r' +', " ", line)
    line = re.sub(r'　+', " ", line)
    line = re.sub(r'\t', " ", line)
    line = re.sub(r'\r', " ", line)
    line = re.sub(r'\n', " ", line)
    line = line.replace('\xa0', ' ')
    return line

def clean(filelist):
    for filename in filelist:
        # if(filename[-3:] == 'sen' or filename[-3:] == 'cle' or filename[-3:] == 'fin' or filename[-3:] == 'tok'): 
        #     continue
        contents = []
        with open(filename, 'r', encoding='utf8') as f:
            for line in f.readlines():
                contents.append(confir(line))

        new_path = './'+filename[:-3][-27:]
        flag = os.path.exists(new_path[:-17])
        if not flag:
            os.mkdir(new_path[:-17])
        with open(new_path+'cle', 'w', encoding='utf8') as f:
            for line in contents:
                f.write(line)

def cleaning(L,R):
    localtime = time.asctime( time.localtime(time.time()) )
    print("Begin read filepath:" + localtime)
    filelist = get_file_list(data_dir,L,R)
    localtime = time.asctime( time.localtime(time.time()) )
    print("End read filepath:" + localtime)
    localtime = time.asctime( time.localtime(time.time()) )
    print("Begin cleaning:"+ localtime)
    clean(filelist)
    localtime = time.asctime( time.localtime(time.time()) )
    print("End cleaning:"+ localtime)