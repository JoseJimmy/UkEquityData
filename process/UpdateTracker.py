import pandas as pd
import os
import shutil
from tqdm import tqdm
from settings import *
def getFileNames(dir, filt_key='.', ext='.csv'):
    Files = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file.lower().count(filt_key.lower()) > 0:
                Files.append(os.path.join(dir, file))
    return Files

def del_files(files_to_delete):
    del_loc = delete_folder
    for file in files_to_delete:
        print('Deleting %s' % file)
        shutil.move(file, del_loc)


def update_tracker_csv():
    files_to_delete = []
    ratio_files = getFileNames(data_folder, 'ratios')
    bal_files = getFileNames(data_folder, 'balance')
    inc_files = getFileNames(data_folder, 'income')
    cash_files = getFileNames(data_folder, 'cash')
    tracker = pd.read_csv(stock_master_csv, index_col='Ticker')
    exclude_list = pd.read_csv(exclude_list_csv, index_col='Ticker')
    tracker = tracker[~tracker.index.isin(exclude_list.index.values)]
    tracker = tracker[['Exchange code'	,'Group'	,'DualListing']]
    # tracker[tracker['DualListing'] == 1].index =  '_'+tracker[tracker['DualListing'] == 1].index
    ## Balance sheet
    for file in tqdm(bal_files, 'Balance data stats'):
        tic = file.split('_')[1]
        if tic in tracker.index:
            tracker.loc[tic, 'Balance'] = 1
        else:
            files_to_delete.append(file)
    del_files(files_to_delete)

    ## Income sheet
    files_to_delete = []
    for file in tqdm(inc_files, 'Income data Stats'):
        tic = file.split('_')[1]
        if tic in tracker.index:
            tracker.loc[tic, 'Income'] = 1
        else:
            files_to_delete.append(file)
    del_files(files_to_delete)

    ## Cash sheet
    files_to_delete = []
    for file in tqdm(cash_files, 'Cash data stats'):
        tic = file.split('_')[1]
        if tic in tracker.index:
            tracker.loc[tic, 'Cash'] = 1
        else:
            files_to_delete.append(file)
    del_files(files_to_delete)

    ## Ratios sheet
    files_to_delete = []

    for file in tqdm(ratio_files, 'Ratio data stats'):
        tic = file.split('_')[1]
        if tic in tracker.index:
            tracker.loc[tic, 'Ratios'] = 1
        else:
            files_to_delete.append(file)
    del_files(files_to_delete)

    tracker.loc[:, 'Price_start'] = pd.to_datetime('01/01/1900')
    tracker.loc[:, 'Price_end'] = pd.to_datetime('01/01/1900')
    tracker.loc[:, 'Price_downloaded'] = 0
    files_to_delete = []
    price_files = getFileNames(price_folder, 'prices', '.csv')
    pbar = tqdm(price_files)
    for file in pbar:
        pbar.set_description("<Prices:%45s>" % file.split('\\')[-1])
        df = pd.read_csv(file, low_memory=False)
        df = df[~(df['TIDM'] == 'TIDM')]
        df = df[~(df['TIDM'] == 'undefinedTIDM')]
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.rename(columns={'TIDM': 'Ticker'})
        df = df.set_index('Ticker')
        tics = df.index.unique()
        for tic in tics:
            if tic in tracker.index:
                if (tracker.loc[tic, 'Price_downloaded']):  # tic prices seen before
                    if tracker.loc[tic, 'Price_start'] > df.loc[tic, 'Date'].min():  # earlier price available check
                        tracker.loc[tic, 'Price_start'] = df.loc[tic, 'Date'].min()
                    if tracker.loc[tic, 'Price_end'] < df.loc[tic, 'Date'].max():  # Later price available check
                        tracker.loc[tic, 'Price_end'] = df.loc[tic, 'Date'].max()

                else:  # tic prices not seen before
                    tracker.loc[tic, 'Price_start'] = df.loc[tic, 'Date'].min()
                    tracker.loc[tic, 'Price_end'] = df.loc[tic, 'Date'].max()
                tracker.loc[tic, 'Price_downloaded'] = 1

    tracker.fillna(0).to_csv(stock_tracker_csv, header=True)
    tracker.fillna(0).to_csv(scrape_list_csv, header=True)

if __name__ == '__main__':
    update_tracker_csv()