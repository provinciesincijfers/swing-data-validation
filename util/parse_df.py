from util.misc import generate_period_list
import pandas as pd
import requests


class Parse_df:
    """
    Class to parse the components of a dataframe that will be used later on in PinC Queries
    Parameters:
    - my_df: dataframe that needs to be parsed
    - _ind_id: indicator for which available list of years needs to be extracted from PinC
    - period: 'table' in case list of years available in dataframe/table can be used in PinC Query, 'pinc' in case
                list of years available in PinC needs to be extracted


    """
    def __init__(self, my_df = None):
        self.my_df = my_df
        if self.my_df is None:
            raise Exception("A dataframe is to be passed as an argument.")
        self.all_pinc_periods = None
        self.ind_id = None
        self.period = None
        self.indicators = []
        self.years = []
        self.pinc_q_years = []
        self.geolevel = None
        self.levels = []
        self.extra_info = {}  # Can bu used to store extra key:value pairs


    def __getitem__(self,key):
        return self.to_dict()[key]

    def __setitem__(self,key, value):
        self.extra_info[key] = value

    def __iter__(self):
        return self.to_dict().__iter__()


    def to_dict(self):
        dic = {'years': self.years, 'indicators': self.indicators, 'geolevel': self.geolevel, 'levels': self.levels}

        for key, val in self.extra_info.items():
            dic[key] =  val
        return dic

    def determine_levels(self):
        self.levels = set(self.my_df['geoitem'])
        return self.levels


    #def determine_years(self, period = 'table', _ind_id = 0):
    def determine_years(self, all_pinc_periods: bool, _ind_id = 0):

        #self.period = period
        self.all_pinc_periods = all_pinc_periods
        begin = self.my_df['period'].astype(int).min()
        end = self.my_df['period'].astype(int).max()

        # Generate period list based on al available years in upload file
        #if self.period == 'table':
        if self.all_pinc_periods == False:
            #begin = self.my_df['period'].astype(int).min()
            #end = self.my_df['period'].astype(int).max()
            period_list_pinc_query, self.years = generate_period_list(begin,end) # --> add to import in .py file
            _ , self.pinc_q_years = generate_period_list(begin,end)
            print(f'List of upload table years: {self.years}')
            return period_list_pinc_query


        # Generate period list based on all available years available in PinC, for _ind_id indicator
        #elif self.period == 'pinc':
        elif self.all_pinc_periods == True:
            # First we fill up the years attribute
            _ , self.years = generate_period_list(begin,end)
            print(f'List of upload table years: {self.years}')
            # Pick (by default the first) available indicator and get the geolevel --> to pass as arg in PinC Query
            self.ind_id = int(_ind_id)
            variable_pinc = self.my_df.columns[3:][self.ind_id]
            self.geolevel = list(self.my_df['geolevel'].unique())[0]
            #print(f'Variable is {variable_pinc}, geolevel is {self.geolevel}')

            # Do PinC Query
            url_string = "https://provincies.incijfers.be/JiveServices/odata/Variables('" + variable_pinc + "')/GeoLevels('" + self.geolevel +"')/PeriodLevels('year')/Periods"
            r = requests.get(url_string)  # --> add request to import in .py file
            r_dict = r.json()

            # Determine period list from PinC Query
            period_list_pinc_query = []
            for i in range(len(r_dict['value'])):
                year = r_dict['value'][i]['FullName']
                period_list_pinc_query.append(year)
            #print(period_list_pinc_query)
            self.pinc_q_years = period_list_pinc_query
            return   ", ".join(period_list_pinc_query)

        else:
            raise Exception("Expected: 'table' or 'pinc' as argument.")


    def determine_indicators(self):
        self.indicators = self.my_df.columns[3:].tolist()
        var_list_pinc_query = ",".join(self.indicators)
        return var_list_pinc_query

    def determine_geolevel(self):
        variable_pinc = self.my_df.columns[3:][self.ind_id]
        self.geolevel = list(self.my_df['geolevel'].unique())[0]
        #print(f'Variable is {variable_pinc}, geolevel is {self.geolevel}')
        return self.geolevel
