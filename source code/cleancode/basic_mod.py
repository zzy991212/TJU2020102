import os
from .config import *
import time
ret = []

def get_file_list(dir,L,R):    
    allfilelist = os.listdir(dir)
    for file in allfilelist:
        filepath = os.path.join(dir,file)
        if os.path.isdir(filepath):
            now_year = int(filepath.split("-")[0][-4:])
            if now_year >= L and now_year <= R:
                get_file_list(filepath,L,R)
        elif os.path.isfile(filepath):
            ret.append(filepath)
    return ret
