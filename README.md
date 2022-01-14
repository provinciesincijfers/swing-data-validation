**Swing data validation**
----
----

Purpose
----
* Create easy to use interface to validate new PinC upload.
* Create playground for PinC-Python enthousiasts


Prerequisites
----
Jupyter notebook or Jupyter-lab


Usage
----

* #### Check PinC Upload 
    1. Place PinC upload (Excel!!!) file 'foo.xlsx' in folder **'upload_pinc'**
    2. Open **Check_PinC_Upload.ipynb**
        
            A. Under 'Parameters/inputs/imports':      
                1. 'Parameters': 'all_pinc_periods = True' (all periods for the indicators available in PinC) or all_pinc_periods = False (same periods as the ones available in foo.xlsx --> based on parsing avaible periods for first indicator)
                2. 'PinC upload file': filename = 'foo.xlsx'
                3. 'Import PinC upload file for validation': set 'sheet_name' by index (int) of by name (str)

               
           B. Click **'Run'-'Run all cells'** or **'Run' - 'Restart Kernel and Run All Cells...'**
           
           C. Intereactive Check Framework
                1. Interactive plot
                2. Interactive overall outlier analysis 
                3. Univariate outlier analysis,


* #### Base(-Dir) variables:
    * Can be found and set in **'settings.py'**

* #### Create level dictionaries:
    * PinC Github levels are placed in '**pinc_github_dir**'
    * Use **'Create_dicts.ipynb'** to create local dictionaries {geo_level_code: geo_level} (e.g. {11001: "Aartselaar", 11002: "Antwerpen", 11004: "Boechout" ,11005: "Boom", ...}) in '**json_config_dir**'.
    * Levels currently available: 'statsec', 'gemeente', 'gemeente2018', 'provincie' and 'arrondiss2018'
    * Note: when adding new geolevels, use PinC geolevel names for creation of geolevel '.json' files: 'pinc_geolevel_name.json'.



Disclaimer:
-----
* The code runs for only 1 geolevel at the time. Ideally there is one upload file per geolevel. In addition, it is possible to have all geolevels included in one upload (Excel file), in such a way that there is one sheet per geolevel. In the latter instance one can iterate over the sheets in the Excel file (by changing the default 'sheet_name=0' to the appropriate index).


Setup:
----

* #### Creation venv:
    conda env create -f environment.yml
* #### Activation venv
    conda activate swing_data_val_env
* #### Deactivation of venv:
    conda deactivate
* #### Remove venv:
    conda remove --name swing_data_val_env --all --yes




Open issues:
----
- [x] Simplify code in notebook (reduce number of lines!)
- [ ] Labels in interactive draw_figure() need to be improved
- [x] draw_figure() as part of misc.py?
- [ ] When loading non consecutive years (e.g. 2013 en 2016), then too many years are shown in the dropdown under outlier analysis.
- [x] Plots: create an overlay (e.g. line with tickers and line without, ...), or automate distance between lines.
- [ ] automatic comparison with higher level (e.g. aggregating values for all municipalities in a province)
- [x] Write more elegant solution for division by zero (resulting in 'inf') issue
- [ ] Automatic test to see if all values for a given geolevel are included in the PinC upload file
- [x] Lange tijdsreeksen volledig opvragen
