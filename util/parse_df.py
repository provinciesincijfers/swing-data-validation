from util.misc import generate_period_list
import pandas as pd
import requests


class Parse_df:
    """
    Class to parse the components of a dataframe that will be used later on in PinC Queries
    Parameters:

    Parameters:
    ------------
    - my_df: pd.dataframe
        Dataframe that needs to be parsed

    Attributes:
    ------------
    - my_df : pd.Dataframe  --> holds the dataframe that is parsed
    - all_pinc_periods : bool  --> compare with all PinC years or not
    - ind_id : int --> which indicator will be used for parsing info (default to 0)
    - indicators : list --> list of uploaded indicators
    - years : list --> list of parsed years
    - pinc_q_years : list --> list of years that will be passed in pinc querry
    - geolevel : str --> geolevel parsed from my_df
    - levels : list --> list of available geolevels in my_df (in fact, code is currently written for only 1 available geolevel)
    - extra_info : dict --> currently not used yet

    Methods:
    ---------
    - to_dict()
    - determine_levels()
    - determine_years()
    - determine_indicators()
    - determine_geolevel()



    """
    def __init__(self, my_df = None):
        self.my_df = my_df
        if self.my_df is None:
            raise Exception("A dataframe is to be passed as an argument.")
        self.all_pinc_periods = None
        self.ind_id = None
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
        ''' Returns different geolevels found in upload file / data_table '''
        self.levels = set(self.my_df['geoitem'])
        return self.levels


    #def determine_years(self, period = 'table', _ind_id = 0):
    def determine_years(self, all_pinc_periods: bool, _ind_id = 0):

        ''' Returns the number of years to be used in PinC Query

        Arguments:
        ----------
        all_pinc_periods : bool
            --> in case of 'True': returns all perionds that can be found in PinC for the respective (_ind_id) indicators
            --> in case of 'False': returns all periods found in the upload dataframe / data_table, based on '_ind_id' indicator
        _ind_id : int --> index of indicator that will be used for years determination
        '''

        self.all_pinc_periods = all_pinc_periods
        begin = self.my_df['period'].astype(int).min()
        end = self.my_df['period'].astype(int).max()

        # Generate period list based on al available years in upload file
        if self.all_pinc_periods == False:
            #begin = self.my_df['period'].astype(int).min()
            #end = self.my_df['period'].astype(int).max()
            period_list_pinc_query, self.years = generate_period_list(begin,end) # --> add to import in .py file
            _ , self.pinc_q_years = generate_period_list(begin,end)
            print(f'List of upload table years: {self.years}')
            return period_list_pinc_query


        # Generate period list based on all available years available in PinC, for _ind_id indicator
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

        #else:
        #    raise Exception("Expected: 'table' or 'pinc' as argument.")


    def determine_indicators(self):
        ''' Returns list of uploaded indicators '''
        self.indicators = self.my_df.columns[3:].tolist()
        var_list_pinc_query = ",".join(self.indicators)
        return var_list_pinc_query

    def determine_geolevel(self):
        ''' Retuns geolevel, parsed from upload dataframe / data_table '''
        variable_pinc = self.my_df.columns[3:][self.ind_id]
        self.geolevel = list(self.my_df['geolevel'].unique())[0]
        #print(f'Variable is {variable_pinc}, geolevel is {self.geolevel}')
        return self.geolevel
