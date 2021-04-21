from settings import CONNECTION_STRING, cash_vars_csv, balance_vars_csv, ratio_vars_csv, income_vars_csv
from sqlalchemy import (MetaData, Table, Column, String,
                        create_engine, Date, Float)
import pandas as pd

def get_schema_vars(file):
    df = pd.read_csv(file, index_col=0)
    col_names = df.index.values
    col_types = [eval(i) for i in df['DataType'].values]
    pkey_flags = [i for i in df['PrimaryKey'].values]
    t_schema = (Column(name, dtype, primary_key=primary_key_flag, )
                for name, dtype, primary_key_flag in zip(col_names, col_types, pkey_flags))
    return t_schema

def get_metaData():
    metadata = MetaData()
    db_Prices = Table('prices', metadata,
                      Column('Ticker', String(30), primary_key=True),
                      Column('Date', Date, primary_key=True),
                      Column('Open', Float),
                      Column('High', Float),
                      Column('Low', Float),
                      Column('Close', Float),
                      Column('Change', Float),
                      Column('Volume', Float),
                      Column('Adjustment', Float))
    db_Ratios = Table('Fund_ratios', metadata, *get_schema_vars(ratio_vars_csv))
    db_Income = Table('Fund_balance', metadata, *get_schema_vars(income_vars_csv))
    db_Balance = Table('Fund_income', metadata, *get_schema_vars(balance_vars_csv))
    db_Cash = Table('Fund_cash', metadata, *get_schema_vars(cash_vars_csv))
    return metadata

