import pickle

import pyautogui
from time import sleep
import os
import pathlib
from datetime import datetime
from settings import *

with open(screen_config_pickle, 'rb') as handle:
    loc_data = pickle.load(handle)


financials_loc = loc_data['financials_loc']
fin_balance_loc = loc_data['fin_balance_loc']
fin_cash_loc = loc_data['fin_cash_loc']
fin_inc_loc = loc_data['fin_inc_loc']
fin_ratios_loc = loc_data['fin_ratios_loc']
fin_sharing_loc = loc_data['fin_sharing_loc']
fin_export_loc = loc_data['fin_export_loc']
prices_loc = loc_data['prices_loc']
prices_sharing_loc = loc_data['prices_sharing_loc']
prices_export_loc = loc_data['prices_export_loc']
prices_export_conf_loc = loc_data['prices_export_conf_loc']
port_add_to_port_loc = loc_data['port_add_to_port_loc']
port_add_muilt_loc = loc_data['port_add_muilt_loc']
port_lookup_loc = loc_data['port_lookup_loc']
port_confirm_loc = loc_data['port_confirm_loc']
first_item = loc_data['first_item']
port_delete_all = loc_data['port_delete_all']
prices_getall_loc = loc_data['prices_getall_loc']
prices_getlast_week_loc = loc_data['prices_getlast_week_loc']
screen_divider_loc = loc_data['screen_divider_loc']


def getFileNames(dir, filt_key='.', ext='.csv'):
    Files = []
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file.lower().count(filt_key.lower()) > 0:
                Files.append(os.path.join(dir, file))
    return Files

def rename_price_files():
    price_files = getFileNames(r"C:\Users\josej\Downloads","price",".csv")
    for file in price_files:
        fname = pathlib.Path(file)
        ctime = datetime.fromtimestamp(fname.stat().st_ctime)
        ctime_str=ctime.strftime("%d-%m-%y_%H%M%S")
        download_dir = r"C:\Users\josej\Downloads"
        new_file_name = "Prices_%s.csv"%ctime_str
        new_file = os.path.join(download_dir, new_file_name)
        os.rename(file,new_file)


def add_to_port(list):
    ##add to port
    pyautogui.click(port_add_to_port_loc, duration=0.1, tween=pyautogui.easeInOutQuad)
    sleep(0.5)
    pyautogui.click(port_add_muilt_loc, duration=0.1, tween=pyautogui.easeInOutQuad)
    pyautogui.write(list)
    sleep(4)
    pyautogui.click(port_lookup_loc, duration=0.1, tween=pyautogui.easeInOutQuad)
    sleep(4)
    pyautogui.click(port_confirm_loc, duration=0.1, tween=pyautogui.easeInOutQuad)

def clear_port():
    ##Clear portfolio
    pyautogui.moveTo(first_item, duration=0.1, tween=pyautogui.easeInOutQuad)
    sleep(1)
    pyautogui.rightClick(first_item, duration=0.1, tween=pyautogui.easeInOutQuad)
    sleep(0.5)
    pyautogui.click(port_delete_all, duration=0.1, tween=pyautogui.easeInOutQuad)


def get_fins(type='balance',test = False):
    loc = fin_balance_loc
    if type == 'income':
        loc = fin_inc_loc
    if type == 'cash':
        loc = fin_cash_loc
    if type == 'ratios':
        loc = fin_ratios_loc
    sleep(0.15)
    pyautogui.click(loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.click(fin_sharing_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(fin_export_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    if(test == False):
        pyautogui.click(fin_export_loc, duration=0.15, tween=pyautogui.easeInOutQuad)

def get_prices(getall = False, test = False):
    pyautogui.moveTo(prices_export_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.click(prices_sharing_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.moveTo(prices_export_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.click(prices_export_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    if getall:
        pyautogui.moveTo(prices_getall_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
        pyautogui.click(prices_getall_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
    else:
        pyautogui.moveTo(prices_getlast_week_loc, duration=0.15, tween=pyautogui.easeInOutQuad)
        pyautogui.click(prices_getlast_week_loc, duration=0.15, tween=pyautogui.easeInOutQuad)

    sleep(0.5)
    if (test == False):
        pyautogui.click(prices_export_conf_loc, duration=0.15, tween=pyautogui.easeInOutQuad)



def goto_loc(loc='finshare'):

    sleep(5);
    screen_divider_loc
    if(loc == 'divider'):
        pyautogui.moveTo(first_item, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(screen_divider_loc, duration=1, tween=pyautogui.easeInOutQuad)
        return

    if(loc == 'finshare'):
        pyautogui.moveTo(first_item, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(fin_sharing_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(first_item, duration=1, tween=pyautogui.easeInOutQuad)
        return

    if(loc == 'priceshare'):
        pyautogui.moveTo(first_item, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(prices_sharing_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(first_item, duration=1, tween=pyautogui.easeInOutQuad)

    if(loc == 'fins'):
        pyautogui.moveTo(fin_inc_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(fin_balance_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(fin_cash_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(fin_ratios_loc, duration=1, tween=pyautogui.easeInOutQuad)
        pyautogui.moveTo(fin_sharing_loc, duration=1, tween=pyautogui.easeInOutQuad)


# Financials Only
def get_financials_list(tic_list,spec,type = 'balance',test=False):
    sleep(5)
    no_tics_per_page = spec['no_tics_per_page']
    y_gap = spec['y_gap']
    pyautogui.click(financials_loc, duration=0.1, tween=pyautogui.easeInOutQuad)
    for lst in tic_list:
        add_to_port(lst)
        sleep(3)

        row_nos = min(len(lst.split(' ')),no_tics_per_page)
        for i in range(0,row_nos):
            pyautogui.moveTo(first_item[0], first_item[1] + (i * y_gap), duration=0.15, tween=pyautogui.easeInOutQuad)
            pyautogui.click(first_item[0], first_item[1] + (i * y_gap), duration=0.15, tween=pyautogui.easeInOutQuad)

            if(type=='income'):
                get_fins('income',test)
                sleep(0.25)


            if(type=='balance'):
                get_fins('balance',test)
                sleep(0.25)


            if(type=='cash'):
                get_fins('cash',test)
                sleep(0.25)

            if(type=='ratios'):
                get_fins('ratios',test)
                sleep(0.25)
        sleep(1)
        clear_port()
        sleep(1)




def get_prices_list(tic_list,spec,test=False):
    no_tics_per_page = spec['no_tics_per_page']
    y_gap = spec['y_gap']
    getall = spec['getfullprices']
    sleep(5)
    pyautogui.click(prices_loc, duration=0.1, tween=pyautogui.easeInOutQuad)
    for lst in tic_list:
        add_to_port(lst)
        sleep(5)
        get_prices(getall,test)
        sleep(40)
        clear_port()
    rename_price_files()
