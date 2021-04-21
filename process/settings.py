from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Date

CONNECTION_STRING = "{drivername}://{user}:{passwd}@{host}:{port}/{db_name}?charset=utf8".format(
    drivername="mysql",
    user="jjimmy",
    passwd="jjjj",
    host="192.168.1.31",
    port="1981",
    db_name="sharedata")

# folder locations
data_folder = r'c:\data\data'
price_folder = r'C:\data\prices'
delete_folder = r'C:\data\to_delete'

ratio_vars_csv = r'c:\data\var_list\Ratios_vars.csv'
income_vars_csv = r'c:\data\var_list\Income_vars.csv'
balance_vars_csv = r'c:\data\var_list\Balance_vars.csv'
cash_vars_csv = r'c:\data\var_list\Cash_vars.csv'



stock_master_csv = r'C:\data\UkSharesMaster.csv'

exclude_list_csv = r'C:\data\download_exclude_list.csv'
stock_tracker_csv = r'C:\data\download_tracker.csv'
scrape_list_csv = r'c:\data\scrapelist.csv'
screen_config_pickle = r'C:\PythonProjects\ShrPadDataProcs\Input\loc_data.pickle'



