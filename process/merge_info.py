import pandas as pd
all_shares_info = pd.read_csv(r"c:\data\AllShares_info.csv", index_col='Ticker')
master = pd.read_csv(r'C:\data\stocks_master_list.csv', index_col='Ticker')
# aim = pd.read_csv(r'C:\data\AIMMAIn.csv', index_col='Ticker')
UkShares = pd.read_csv(r'C:\data\UkShares.csv', index_col='Ticker')

new_mast = all_shares_info[all_shares_info.index.isin(master.index)].copy()
new_mast.insert(1,'DualListing',0)
new_mast.loc[new_mast.index.duplicated(),'DualListing'] = 1
new_mast.index.values[new_mast.index.duplicated()] = '_'+new_mast.loc[new_mast.index.duplicated()].index

new_mast = new_mast.join(aim['LSE listing'])
new_mast.insert(1,'Group',new_mast['LSE listing'].fillna(new_mast['Exchange code']))
new_mast.sort_values(by = ['Exchange code','Group','Ticker'],inplace=True)
new_mast.drop(columns = 'LSE listing').to_csv(r'c:\data\stocks_master_list.csv')
