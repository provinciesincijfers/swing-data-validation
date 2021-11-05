import pandas as pd

from  matplotlib.ticker import FuncFormatter # needed to set tickers properly in interactive plots
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")




def draw_figure(var : str ,geo : str, var_dic : dict, geo_dic : dict, pinc_table: pd.DataFrame, data_table: pd.DataFrame, constant : int):
    tmp_df = pd.DataFrame()
    
    upload_var = var_dic.get(var)
    upload_geo = geo_dic.get(geo)
    
    tmp_df_pinc = pinc_table[pinc_table['Geo']==geo][['Perioden','Geo',var]]
    tmp_df_pinc['Geo'] = tmp_df_pinc['Geo'].apply(lambda x: str(x) + '_PinC')
    tmp_df_pinc[var] = tmp_df_pinc[var].apply(lambda x: None if ((not x) or (x=='-') or (x=='x') or (x=='?')) else (float(x) + constant) )  # We add one to ease comparison in plot
    tmp_df = tmp_df.append(tmp_df_pinc)
    #print('PinC Dataframe:')
    #print(tmp_df.head())
    
    tmp_df_upload = data_table[data_table['geoitem']==upload_geo][['period','geoitem',upload_var]]
    tmp_df_upload = tmp_df_upload.rename(columns={'geoitem':'Geo', 'period': 'Perioden', upload_var : var})
    tmp_df_upload['Geo'] = tmp_df_upload['Geo'].apply(lambda x: str(x) + '_Upload')
    tmp_df_upload[var] = tmp_df_upload[var].apply(lambda x: float(x))
    tmp_df = tmp_df.append(tmp_df_upload)
    #print('Upload Dataframe:')
    #print(tmp_df.head())
    
    tmp_df['Perioden'] = tmp_df['Perioden'].apply(lambda x: int(x))
    #print(tmp_df['Perioden'].unique())
    sns.lineplot(data=tmp_df, x='Perioden',y= var,hue='Geo', style='Geo', markers=True, dashes=False);
    # Format year on xticks to int (instead of float):
    plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: int(x)));
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.);