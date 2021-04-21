import pickle
import pandas as pd
from Input.scraper_helpers import *
from processing.UpdateTracker import update_tracker_csv
from settings import *
from datetime import datetime, timedelta

if __name__ == '__main__':

    y_gap = 25
    no_tics_per_page = 20

    tracker = pd.read_csv(scrape_list_csv,parse_dates=['Price_start', 'Price_end', 'Price_downloaded'])

    bal_tics = tracker[tracker.Balance==0].Ticker#[0:6]
    bal_tics = bal_tics[~bal_tics.str.contains('_')]

    inc_tics = tracker[tracker.Income==0].Ticker#[0:6]
    inc_tics = inc_tics[~inc_tics.str.contains('_')]

    cash_tics = tracker[tracker.Cash==0].Ticker#[0:6]
    cash_tics = cash_tics[~cash_tics.str.contains('_')]

    rat_tics = tracker[tracker.Ratios==0].Ticker#[0:6]
    rat_tics = rat_tics[~rat_tics.str.contains('_')]

    fin_tics = {'income':inc_tics,'balance':bal_tics,'cash':cash_tics,'ratios':rat_tics}
    fin_screen_spec = {'y_gap' :  25, 'no_tics_per_page' : 20}
    no_tics_per_page = fin_screen_spec['no_tics_per_page']

    ##################################################################
    #  Fins
    #
    ##################################################################
    # fins_to_grab = ['balance','income','cash','ratios']
    # fins_to_grab = []
    # for f_type in fins_to_grab:
    #     tics = fin_tics[f_type]
    #     tics_str_list = [' '.join(tics.iloc[i:i + no_tics_per_page]) for i in range(0, len(tics), no_tics_per_page)]
    #     get_financials_list(tics_str_list,fin_screen_spec,f_type,False,)


    ##################################################################
    #  Prices
    #
    ##################################################################

    get_empty_prices = 1
    update_stale_prices = 0

    if get_empty_prices:
        prices_screen_spec = {'y_gap': 25, 'no_tics_per_page': 98, 'getfullprices': True}
        no_tics_per_page = prices_screen_spec['no_tics_per_page']
        tics = tracker[tracker.Price_downloaded == '0'].Ticker
        tics_str_list = [' '.join(tics.iloc[i:i + no_tics_per_page]) for i in range(0, len(tics), no_tics_per_page)]
        get_prices_list(tics_str_list,prices_screen_spec, test=False)

    if update_stale_prices:
        prices_screen_spec = {'y_gap': 25, 'no_tics_per_page': 98, 'getfullprices': False}
        no_tics_per_page = prices_screen_spec['no_tics_per_page']
        stale_dates_mask = tracker.Price_end < datetime.today() - timedelta(days=+2)
        tics = tracker[stale_dates_mask].Ticker
        tics_str_list = [' '.join(tics.iloc[i:i + no_tics_per_page]) for i in range(0, len(tics), no_tics_per_page)]
        get_prices_list(tics_str_list,prices_screen_spec, test=False)




    os.system('shutdown /s /f ')






