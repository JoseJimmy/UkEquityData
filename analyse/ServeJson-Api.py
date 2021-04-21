from sqlalchemy import create_engine, Table, select, and_, desc
from tqdm import tqdm

from utils.dbConnect import get_metaData
from settings import CONNECTION_STRING
from settings import stock_master_csv, exclude_list_csv
import pandas as pd
from datetime import datetime, timedelta


def getLastAvailDate():
    s = select([Prices.c.Date]).distinct();
    s = s.order_by(desc(Prices.c.Date)).limit(5)
    df = pd.read_sql(s, connection, parse_dates='Date')
    return df.max()


## Base data
##
stocks = pd.read_csv(stock_master_csv)
stocks.Ticker = stocks['Exchange code'] + ':' + stocks.Ticker.values
stocks = stocks.reset_index().set_index(['Market', 'TicType', 'Industry', 'Sector']).sort_index()




## Prep Variant keys for
end_date = pd.to_datetime('04/01/2021')
start_dates = {"1M":end_date - timedelta(days=30),
               "3M":end_date - timedelta(days=90),
               "6M":end_date - timedelta(days=180),
               "1Y":end_date - timedelta(days=365),
               "2Y":end_date - timedelta(days=730),
               "3Y":end_date - timedelta(days=1095),
               "5Y":end_date - timedelta(days=1830)}
markets = ['AIM','Full']
retsTsJson = {'AIM':"retTsDataAim.Json","Full":"retTsDataFull.Json"}
treeNavJson = {'AIM':"treeNavAim.Json","Full":"treeNavFull.Json"}


## Connect to database
engine = create_engine(CONNECTION_STRING)
connection = engine.connect()
metadata = get_metaData()
metadata.create_all(engine)
Prices = Table('Prices', metadata, autoload=True, autoload_with=engine)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Tree Nav  Data Json Api : Data List
# parent, id,Name,Ticker ,TicType,Period returns (%),Volatility (%)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def periodRet(df):
    x = df.fillna(0).sort_index(ascending=True)
    x = (1+(x*0.01)).cumprod()
    return (x.iloc[-1]-1).round(5)

def periodLogRet(df):
    x = df.fillna(0).sort_index(ascending=True)
    x = (1+(x*0.01)).cumprod()
    return (x.iloc[-1]-1).round(5)

def periodVol(df):
    x = df.fillna(0)*0.01;
    return x.std().round(4)

for mkt in tqdm(markets):
    selectTics, df ,rets,vol= [], [],[], [];

    selectTics = stocks.loc[mkt][['Ticker', 'Name', 'id', 'parent']].sort_values('id').copy(deep=True)
    cols = ['parent', 'id', 'Name', 'Ticker', 'TicType'];

    for period in start_dates.keys():
        start_date = start_dates[period]
        s = select([Prices.c.Date, Prices.c.Ticker, Prices.c.Close, Prices.c.Change]).where(and_(
            Prices.c.Date.between(start_date, end_date), Prices.c.Ticker.in_(selectTics.Ticker)))
        s = s.order_by(Prices.c.Date)
        df = pd.read_sql(s, connection, parse_dates='Date').set_index('Date')
        rets = df.groupby('Ticker').agg({'Change': periodRet}).rename(columns = {'Change':"ret_"+period})
        selectTics = selectTics.join(rets, on='Ticker', how='left')
        cols.append("ret_"+period)
        vol = df.groupby('Ticker').agg({'Change': periodVol}).rename(columns = {'Change':"vol_"+period})
        selectTics = selectTics.join(vol, on='Ticker', how='left')
        cols.append("vol_"+period)
    selectTics.reset_index()[cols].to_json(treeNavJson[mkt],orient='records')

# #  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #  Price Chart  Data Json Api
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#### For time series charts
selectTics = [];
Periods = ['5Y']
for mkt in tqdm(markets):
    for period in Periods:
        selectTics,df=[],[]
        selectTics = stocks.loc[mkt][['Ticker', 'Name', 'id', 'parent']].sort_values('id').copy(deep=True)
        tic2id_dict = selectTics[['Ticker', 'id']].reset_index(drop=True).set_index('Ticker').sort_values('Ticker').to_dict('dict')['id']

        cols = ['parent', 'id', 'Name', 'Ticker', 'TicType']
        start_date = start_dates[period]
        tic2id_dict = selectTics[['Ticker', 'id']].reset_index(drop=True).set_index('Ticker').sort_values('Ticker').to_dict('dict')['id']

        s = select([Prices.c.Date, Prices.c.Ticker, Prices.c.Close, Prices.c.Change]).where(and_(
            Prices.c.Date.between(start_date, end_date), Prices.c.Ticker.in_(selectTics.Ticker)))
        s = s.order_by(Prices.c.Date)
        df = pd.read_sql(s, connection, parse_dates='Date')
        df['Week_Number'] = df['Date'].dt.isocalendar().week
        df['Year'] = df['Date'].dt.year
        df = df.groupby(['Year', 'Week_Number', 'Ticker']).agg({'Change': periodRet, 'Close': 'last', 'Date': 'max'})
        df = df.reset_index().drop(columns=['Year', 'Week_Number']).sort_values(by=['Ticker', 'Date'])
        df['Date']= df['Date'].dt.strftime('%Y-%m-%d')
        df = df.rename(columns={'Ticker': 'id'}).replace({'id': tic2id_dict})
        df.to_json(retsTsJson[mkt].replace(".Json", period + ".Json"), orient='records')


