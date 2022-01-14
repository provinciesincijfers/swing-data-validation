import json
import pandas as pd
import numpy as np




from  matplotlib.ticker import FuncFormatter # needed to set tickers properly in interactive plots
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")


from settings import PINC_GITHUB_DIR, JSON_CONF_DIR, UPLOAD_DIR
from util.misc import read_json_file

class Conn_pinc_data(object):
    """
    Class to connect pinc dataframe with upload file dataframe, in order to visualize similarities and
    detect differences.

    Parameters:
    ------------
    - pinc_df : pd.Dataframe --> DataFrame, obtained from PinC querry
    - upload_df : pd.Dataframe --> Upload DataFrame
    - level : str --> geolevel on which comparison will be conducted

    Attributes:
    -----------
    - pinc_df : pd.DataFrame
    - upload_df : pd.DataFrame
    - level : str
    - cols_dic: dict --> dictionary that will be used to store (pinc_indicator_name : upload_indicator_name) pairs

    Methods:
    ---------
    - cols_to_dict()
    - reversed_cols_to_dict()
    - level_code_dict()
    - reversed_level_code_dict()
    - draw_figure()
    - overall_outlier_analysis()
    - show_outliers()

    """
    def __init__(self, pinc_df = None, upload_df = None, level = None):
        self.pinc_df = pinc_df
        if self.pinc_df is None:
            raise Exception("A PinC dataframe is to be passed as an argument.")
        self.upload_df = upload_df
        if self.upload_df is None:
            raise Exception("An upload file dataframe is to be passed as an argument.")
        self.level = level
        #self.cols = None
        self.cols_dic = {}
        #self.extra_info = {}  # Can bu used to store extra key:value pairs

#### HIER GEKOMEN, NET IF NOT SELF.COLS_DIC: CONDITIE TOEGEVOEGD
    def cols_to_dict(self):
        ''' Load self.cols_dic dictionary with (pinc_indicator_name, upload_indicator_name) pairs
        and return dictionary '''
        dic = {key:value for (key, value) in zip(self.pinc_df.columns[2:].tolist(),self.upload_df.columns[3:].tolist())}
        #for key, val in self.extra_info.items():
        #    dic[key] =  val
        self.cols_dic = dic
        return dic

    def reversed_cols_to_dict(self):
        ''' Return dictionary with (upload_indicator_name, pinc_indicator_name) pairs '''
        dic = {value:key for (key, value) in zip(self.pinc_df.columns[2:].tolist(),self.upload_df.columns[3:].tolist())}
        return dic

    #@staticmethod
    #def level_code_dict(level= None):
    def level_code_dict(self):
        ''' Return geolevel dictionary '''
        #Available levels: statsec, gemeente, provincie, arrondissement
        if self.level is None:
            raise Exception("A geolevel is to be passed as an argument to the class constructor.")

        else:
            level_code_dict = read_json_file(self.level)
            return level_code_dict


    #@staticmethod
    #def reversed_level_code_dict(level= None):
    def reversed_level_code_dict(self):
        ''' Return reversed geolevel dictionary '''
        #Available levels: statsec, gemeente, provincie, arrondissement
        if self.level is None:
            raise Exception("A geolevel is to be passed as an argument to the class constructor.")

        else:
            level_code_dict = read_json_file(self.level)
            reversed_level_code_dict = {y:x for x,y in level_code_dict.items()}
            return reversed_level_code_dict




    def draw_figure(self, var: str ,geo : str, constant : float):
        ''' Draw interactive plot

        Parameters:
        ------------
        - var : str --> indicator to be plotted
        - geo : str --> geolevel value to be plotted
        - constant : int --> integer difference between plot lines

        Returns:
        ---------
        - interactive plot

        '''
        t_df = pd.DataFrame()

        upload_var = self.cols_dic.get(var)
        upload_geo = self.reversed_level_code_dict().get(geo)

        t_df_p = self.pinc_df[self.pinc_df['Geo']==geo][['Perioden','Geo',var]]
        t_df_p['Geo'] = t_df_p['Geo'].apply(lambda x: str(x) + '_PinC')
        t_df_p[var] = t_df_p[var].apply(lambda x: None if ((not x) or (x=='-') or (x=='x') or (x=='?')) else (float(x) + constant) )  # We add constant to ease comparison in plot
        t_df = t_df.append(t_df_p)
        #print('PinC Dataframe:')
        #print(tmp_df.head())

        t_df_u = self.upload_df[self.upload_df['geoitem']==upload_geo][['period','geoitem',upload_var]]
        t_df_u = t_df_u.rename(columns={'geoitem':'Geo', 'period': 'Perioden', upload_var : var})
        t_df_u['Geo'] = t_df_u['Geo'].apply(lambda x: str(x) + '_Upload')
        t_df_u[var] = t_df_u[var].apply(lambda x: float(x))
        t_df = t_df.append(t_df_u)
        #print('Upload Dataframe:')
        #print(tmp_df.head())

        t_df['Perioden'] = t_df['Perioden'].apply(lambda x: int(x))
        #print(tmp_df['Perioden'].unique())
        sns.lineplot(data=t_df, x='Perioden',y= var,hue='Geo', style='Geo', palette = 'deep', markers=True, markersize=13, alpha=0.5, dashes=[(1, 1), (2, 2)]);
        # Format year on xticks to int (instead of float):
        plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)));
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);






    def overall_outlier_analysis(self, pinc_year : int, upload_year : int, absolute: bool, ignore_inf = False):
        ''' Draw interactive plot for overall outlier analysis

        Parameters:
        -----------
        - pinc_year : str
        - upload_year : str
        - absolute : bool --> plot absolute or relative differences
        - ingore_inf : bool --> ingore inf values (because of division by zero) in plot or # NOTE:

        Returns:
        ---------
        - interactive plot

        '''
        t_df = pd.DataFrame()
        tel = 0
        for var in list(self.cols_dic.keys()):
            upload_var = self.cols_dic.get(var)

            t_df_p = self.pinc_df[self.pinc_df['Perioden']==str(pinc_year)][['Geo',var]]
            t_df_p[var] = t_df_p[var].apply(lambda x: None if ((not x) or (x=='-') or (x=='x') or (x=='?')) else (float(x) ) )
            t_df_p = t_df_p[t_df_p[var]!=-99996]
            t_df_p = t_df_p.rename(columns={'Geo':'Geo_pinc',var: '_pinc_' + str(pinc_year)})
            t_df_p['geo_code_pinc'] = t_df_p['Geo_pinc'].map(self.reversed_level_code_dict())


            t_df_u = self.upload_df[self.upload_df['period']==str(upload_year)][['geoitem',upload_var]]
            t_df_u = t_df_u.rename(columns={'geoitem':'geo_code_upload', upload_var : '_upload_' + str(upload_year)})
            t_df_u['_upload_' + str(upload_year)] = t_df_u['_upload_' + str(upload_year)].apply(lambda x: float(x))

            m_df = t_df_p.merge(t_df_u, left_on='geo_code_pinc', right_on='geo_code_upload')
            m_df['diff_rel'] = abs(m_df['_pinc_' + str(pinc_year)]-m_df['_upload_' + str(upload_year)])/m_df['_pinc_' + str(pinc_year)]
            m_df['diff_abs'] = abs(m_df['_pinc_' + str(pinc_year)]-m_df['_upload_' + str(upload_year)])
            m_df['Indicator'] = var + '_P' + str(pinc_year) + '_U' + str(upload_year)

            ## Uncomment next line for some validation
            #print(f'Variable: {var}, Shape: {merged_df.shape}')
            tel += m_df.shape[0]
            t_df = t_df.append(m_df)

        ## Uncomment two next lines for some counters to be used for validation:
        #tel_t = len(list(var_dic.keys())*merged_df.shape[0])
        #print(f'Cumulated no. rows: {tel} vs theoretical no. rows: {tel_t}')

        if absolute:
            print('Absolute difference evaluation')
            # Uncomment second line if you want to ignore diff=inf as a result from division by zero
            # Uncomment third line if you  also (in addition to previous condition) want to ignore PinC missing values [-99996, -99997, -99998, -99999] in upload file
            if ignore_inf == False:
                return t_df.sort_values(by=['diff_abs'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_abs','Indicator']].head(30)
            else:
                return t_df[~(t_df['diff_abs']==np.inf)].sort_values(by=['diff_abs'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_abs','Indicator']].head(30)
            #return t_df[~((t_df['diff_rel']==np.inf) | (t_df['_upload_' + str(upload_year)].isin(PINC_MV_L)))].sort_values(by=['diff_rel'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_rel','Indicator']].head(30)
        else:
            print('Relative difference evaluation')
            # Uncomment second line if you want to ignore diff=inf as a result from division by zero
            # Uncomment third line if you  also (in addition to previous condition) want to ignore PinC missing values [-99996, -99997, -99998, -99999] in upload file
            if ignore_inf == False:
                return t_df.sort_values(by=['diff_rel'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_rel','Indicator']].head(30)
            else:
                return t_df[~(t_df['diff_rel']==np.inf)].sort_values(by=['diff_rel'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_rel','Indicator']].head(30)
            #return t_df[~((t_df['diff_rel']==np.inf) | (t_df['_upload_' + str(upload_year)].isin(PINC_MV_L)))].sort_values(by=['diff_rel'], ascending=False)[['Geo_pinc', '_pinc_' + str(pinc_year), '_upload_' + str(upload_year),'diff_rel','Indicator']].head(30)




    def show_outliers(self, var : str, upload_year : int , pinc_year : int):
        ''' Draw interactive plot for univariate outlier analysis

        Parameters:
        ------------
        - var : str
        - upload_year : int
        - pinc_year : int

        Returns:
        ---------
        - interactive plot

        '''
        upload_var = self.cols_dic.get(var)
        #upload_var = var_dic.get(var)

        t_df_p = self.pinc_df[self.pinc_df['Perioden']==str(pinc_year)][['Geo',var]]
        t_df_p[var] = t_df_p[var].apply(lambda x: None if ((not x) or (x=='-') or (x=='x') or (x=='?')) else (float(x) ) )
        t_df_p = t_df_p.rename(columns={'Geo':'Geo_pinc',var: var + '_pinc_' + str(pinc_year)})
        t_df_p['geo_code_pinc'] = t_df_p['Geo_pinc'].map(self.reversed_level_code_dict())


        t_df_u = self.upload_df[self.upload_df['period']==str(upload_year)][['geoitem',upload_var]]
        t_df_u = t_df_u.rename(columns={'geoitem':'geo_code_upload', upload_var : var + '_upload_' + str(upload_year)})
        t_df_u[var + '_upload_' + str(upload_year)] = t_df_u[var + '_upload_' + str(upload_year)].apply(lambda x: float(x))

        m_df = t_df_p.merge(t_df_u, left_on='geo_code_pinc', right_on='geo_code_upload')
        m_df['diff'] = abs(m_df[var + '_pinc_' + str(pinc_year)]-m_df[var + '_upload_' + str(upload_year)])/m_df[var + '_pinc_' + str(pinc_year)]
        #return merged_df.sort_values(by=['diff'], ascending=False)[['Geo_pinc', var + '_pinc_' + str(pinc_year), var + '_upload_' + str(upload_year),'diff']].head(20)
        return m_df[~(m_df['diff']==np.inf)].sort_values(by=['diff'], ascending=False)[['Geo_pinc', var + '_pinc_' + str(pinc_year), var + '_upload_' + str(upload_year),'diff']].head(20)
