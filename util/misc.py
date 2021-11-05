
import json
import pandas as pd
from  matplotlib.ticker import FuncFormatter

from settings import PINC_GITHUB_DIR, JSON_CONF_DIR, UPLOAD_DIR, BASE_YEAR


'''
Function for period list generation:
Usage: obj = generate_period_list(begin_year, end_year)
'''
def generate_period_list(begin=BASE_YEAR, end=BASE_YEAR):
    if (begin == end):
        period_list = str(begin)
        return period_list, str(begin)
    else:
        tmp_list = list(range(begin,end+1))
        #print(tmp_list)
        s = [str(i) for i in tmp_list]
        period_list = ", ".join(s)
        return period_list, s


def read_json_file(name='gemeente'):
    jf = JSON_CONF_DIR + '/' + name + '.json'
    with open(jf) as f:
        json_dict = json.load(f)
    return json_dict


def write_json_file(dic, name_file):
    assert isinstance(dic,dict), "Dictionary expected as input!"
    if len(name_file.split('.')) > 1:
        of = JSON_CONF_DIR + '/' + name_file.split('.')[0] + '.json'
        print(f'Writing to: {of}')
    else :
        of = JSON_CONF_DIR + '/' + name_file + '.json'
        print (f'Writing to: {of}')
    with open(of, 'w') as fp:
        json.dump(dic, fp, indent=4)
