from tqdm import tqdm
from helper_fncs import *
from sqlalchemy import (MetaData, Table, Column, create_engine)
from settings import *
import pandas as pd
import os
import shutil
import numpy as np
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Date , Float
from pandas.errors import EmptyDataError
from sqlalchemy.dialects.mysql import insert

###################################################################################
# Create Schema
###################################################################################

## Ratios variables
def create_schema_csv(files, tag='Default'):
    date_cols = ['Year', 'Period Ending']
    vars_list = pd.DataFrame([])
    pbar = tqdm(files)
    for file in pbar:
        pbar.set_description("Processing var list/schema %s files " % tag)
        df = fetch_csv_df(file, date_cols)
        if (df.empty == 0):
            df = df_column_uniquify(df)
            vals = df['Result Type'].str.split(' ').str[0].str.strip()
            df.insert(3, 'Result Quarter', vals)
            vals = df['Result Type'].str.split(' ').str[1].str.strip()
            df.insert(3, 'Ac Standard', vals)
            df.columns = df.columns.str.strip().str.replace('%', '[pct]')
            tic = df.Ticker.iloc[0]
            tic = exchange_dict[tic]
            tdf = pd.DataFrame(index=df.columns, columns=[tic])
            tdf[tic] = 1
            vars_list = pd.concat([vars_list, tdf], axis=1)

    vars_list = vars_list.fillna(0)  # .T
    vars_list.insert(0, 'Total', vars_list.sum(axis=1))
    vars_list.insert(1, 'DataType', 'Float')
    vars_list.insert(1, 'PrimaryKey', 'False')
    vars_list.loc['Ticker', 'DataType'] = 'String(30)'
    vars_list.loc['Year', 'DataType'] = 'Date'
    vars_list.loc['Period Ending', 'DataType'] = 'Date'
    vars_list.loc['Result Type', 'DataType'] = 'String(20)'
    vars_list.loc['Ac Standard', 'DataType'] = 'String(8)'
    vars_list.loc['Result Quarter', 'DataType'] = 'String(8)'
    vars_list.loc['Ticker', 'PrimaryKey'] = 'True'
    vars_list.loc['Period Ending', 'PrimaryKey'] = 'True'
    return vars_list


def get_schema_vars(file):
    df = pd.read_csv(file, index_col=0)
    col_names = df.index.values
    col_types = [eval(i) for i in df['DataType'].values]
    pkey_flags = [i for i in df['PrimaryKey'].values]
    t_schema = (Column(name, dtype, primary_key=primary_key_flag, )
                for name, dtype, primary_key_flag in zip(col_names, col_types, pkey_flags))
    return t_schema


## Ratios variables
def get_fin_data_df(files, tag='Default'):
    date_cols = ['Year', 'Period Ending']
    full_df = pd.DataFrame([])
    for file in files:
        df = fetch_csv_df(file, date_cols)
        if (df.empty == 0):
            df = df_column_uniquify(df)
            vals = df['Result Type'].str.split(' ').str[0].str.strip()
            df.insert(3, 'Result Quarter', vals)
            vals = df['Result Type'].str.split(' ').str[1].str.strip()
            df.insert(3, 'Ac Standard', vals)
            df.columns = df.columns.str.strip().str.replace('%', '[pct]')
            tic = df.Ticker.iloc[0]
            tic = exchange_dict[tic]
            df['Ticker'] = tic
            data_cols = df.columns[6:]  # specify columns you want to replace
            df[data_cols] = df[data_cols].replace('>+', '', regex=True)
            df[data_cols] = df[data_cols].replace({'Infinity': None, '-Infinity': None})
            df[data_cols] = df[data_cols].replace({})

            full_df = full_df.append(df)
            full_df = full_df.where((pd.notnull(full_df)), None)
    return full_df


###################################################################################
# Create Schema in csv file
###################################################################################

exchange_dict = tic_to_exchange()
ratio_files = getFileNames(data_folder, 'ratios')
bal_files = getFileNames(data_folder, 'balance')
inc_files = getFileNames(data_folder, 'income')
cash_files = getFileNames(data_folder, 'cash')
price_files = getFileNames(data_folder, 'prices')

## Create Scheme_csv
create_schema_csv(ratio_files, 'ratio').to_csv(ratio_vars_csv)
create_schema_csv(bal_files, 'balance').to_csv(balance_vars_csv)
create_schema_csv(inc_files, 'income').to_csv(income_vars_csv)
create_schema_csv(cash_files, 'cash').to_csv(cash_vars_csv)

###################################################################################
# DB Connection and define table
###################################################################################

engine = create_engine(CONNECTION_STRING)
connection = engine.connect()
metadata = MetaData()

Ratios = Table('Fund_ratios', metadata, *get_schema_vars(ratio_vars_csv))
Income = Table('Fund_balance', metadata, *get_schema_vars(income_vars_csv))
Balance = Table('Fund_income', metadata, *get_schema_vars(balance_vars_csv))
Cash = Table('Fund_cash', metadata, *get_schema_vars(cash_vars_csv))
metadata.create_all(engine)

###################################################################################
# process csv to db
###################################################################################

for file in tqdm(ratio_files, 'Processing Ratio Data'):
    df = get_fin_data_df([file])
    if (df.empty == False):
        insert_stmt = insert(Ratios).values(df.to_dict('records'))
        update_dict = {x.name: x for x in insert_stmt.inserted}
        upsert_query = insert_stmt.on_duplicate_key_update(update_dict)
        result = connection.execute(upsert_query)

for file in tqdm(bal_files, 'Processing Balans Data'):
    df = get_fin_data_df([file])
    if (df.empty == False):
        insert_stmt = insert(Balance).values(df.to_dict('records'))
        update_dict = {x.name: x for x in insert_stmt.inserted}
        upsert_query = insert_stmt.on_duplicate_key_update(update_dict)
        result = connection.execute(upsert_query)

for file in tqdm(inc_files, 'Processing Income Data'):
    df = get_fin_data_df([file])
    if (df.empty == False):
        insert_stmt = insert(Income).values(df.to_dict('records'))
        update_dict = {x.name: x for x in insert_stmt.inserted}
        upsert_query = insert_stmt.on_duplicate_key_update(update_dict)
        result = connection.execute(upsert_query)

for file in tqdm(cash_files, 'Processing Cash Data'):
    df = get_fin_data_df([file])
    if (df.empty == False):
        insert_stmt = insert(Cash).values(df.to_dict('records'))
        update_dict = {x.name: x for x in insert_stmt.inserted}
        upsert_query = insert_stmt.on_duplicate_key_update(update_dict)
        result = connection.execute(upsert_query)

connection.close()
