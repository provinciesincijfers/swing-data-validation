import json
from settings import PINC_GITHUB_DIR, JSON_CONF_DIR, UPLOAD_DIR
from util.misc import read_json_file

class Conn_pinc_data(object):
    """
    Class to connect pinc dataframe with upload file dataframe, in order to visualize similarities and 
    detect differences.
    
    """
    def __init__(self, pinc_df = None, upload_df = None):
        self.pinc_df = pinc_df
        if self.pinc_df is None:
            raise Exception("A PinC dataframe is to be passed as an argument.")
        self.upload_df = upload_df
        if self.upload_df is None:
            raise Exception("An upload file dataframe is to be passed as an argument.")
        self.level = None
        self.cols = None
        self.cols_dic = {}
        self.extra_info = {}  # Can bu used to store extra key:value pairs
        
        
    def cols_to_dict(self):
        dic = {key:value for (key, value) in zip(self.pinc_df.columns[2:].tolist(),self.upload_df.columns[3:].tolist())}
        
        for key, val in self.extra_info.items():
            dic[key] =  val
        self.cols_dic = dic
        return dic
    
    def reversed_cols_to_dict(self):
        dic = {value:key for (key, value) in zip(self.pinc_df.columns[2:].tolist(),self.upload_df.columns[3:].tolist())}
        return dic
        
    @staticmethod
    def level_code_dict(level= None):
        #Available levels: statsec, gemeente, provincie, arrondissement
        if level is None:
            raise Exception("A geolevel is to be passed as an argument.")

        else:
            level_code_dict = read_json_file(level)
            return level_code_dict
        
    
    @staticmethod
    def reversed_level_code_dict(level= None):
        #Available levels: statsec, gemeente, provincie, arrondissement
        if level is None:
            raise Exception("A geolevel is to be passed as an argument.")

        else:
            level_code_dict = read_json_file(level)
            reversed_level_code_dict = {y:x for x,y in level_code_dict.items()}
            return reversed_level_code_dict
                
            
    def outlier_analysis(self, cols='all', pinc_year=None, upload_year=None):
        self.cols = cols
        if self.cols == 'all':
            print('All columns at the same time is requested')
        elif self.cols == 'obo':
            print('One column at the time is requested')
        elif isinstance(self.cols, list):
            print('List is requested')
        else:
            raise Exception("Different argument expected: 'all', 'obo' or input list.")