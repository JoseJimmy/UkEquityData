import pandas as pd
import os
import shutil
import numpy as np
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Date
from pandas.errors import EmptyDataError
from sqlalchemy.dialects.mysql import insert
from settings import *


def load_tracker():
    tracker = pd.read_csv(stock_tracker_csv,index_col = 'Ticker')
    for col in ['Price_start','Price_end']:
        tracker[col] = pd.to_datetime(tracker[col])
    tic2exch_dict = tracker['Exchange code'].to_dict()
    tic2exch_dict = {k: v + ':' + k for k, v in tic2exch_dict.items()}
    tracker = tracker.reset_index().replace({'Ticker': tic2exch_dict})
    return tracker.set_index('Ticker').drop(columns=['Exchange code'])


def tic_to_exchange():
    tracker = pd.read_csv(stock_tracker_csv, index_col='Ticker')
    exchange_dict = tracker['Exchange code'].to_dict()
    return {k: v + ':' + k for k, v in exchange_dict.items()}



def getFileNames(dir, filt_key='.', ext='.csv'):
    Files = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file.lower().count(filt_key.lower()) > 0:
                Files.append(os.path.join(dir, file))
    return Files


def fetch_csv_df(file, date_cols):
    tic = file.split('_')[1]
    try:
        df = pd.read_csv(file, index_col=0, header=None).T
    except EmptyDataError:
        return pd.DataFrame([])
    df.insert(loc=0, column='Ticker', value=tic)
    for col in date_cols:
        df[col] = pd.to_datetime(df[col])
    return df



def df_column_uniquify(df):
    df_columns = df.columns
    new_columns = []
    for item in df_columns:
        counter = 0
        newitem = item
        while newitem in new_columns:
            counter += 1
            newitem = "{}_{}".format(item, counter)
        new_columns.append(newitem)
    df.columns = new_columns
    return df