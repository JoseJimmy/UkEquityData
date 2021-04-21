import winsound
import math
import pyautogui
from time import sleep
from time import sleep
import pandas as pd
import tkinter as tk
import pickle


##Calibration
from settings import *


def get_manual_homeloc(name, delay=3):
    root = tk.Tk()
    root.title("Info")
    tk.Label(root, text='Browse to %s' % name).pack()
    root.after(4000, lambda: root.destroy())  # time in ms
    root.mainloop()
    for i in range(0, delay):
        sleep(1)
        winsound.Beep(400, 50)
    winsound.Beep(500, 500)
    loc = pyautogui.position()
    return (loc)


sleep(5)
loc_data={}
loc_data['financials_loc'] = get_manual_homeloc('financial')
loc_data['fin_balance_loc'] = get_manual_homeloc('Balance')
loc_data['fin_cash_loc'] = get_manual_homeloc('Cash')
loc_data['fin_inc_loc'] = get_manual_homeloc('Income')
loc_data['fin_ratios_loc'] = get_manual_homeloc('Ratios')
loc_data['fin_sharing_loc'] = get_manual_homeloc('Fin Sharing')
loc_data['fin_export_loc'] = get_manual_homeloc('Fin Export')
loc_data['prices_loc'] = get_manual_homeloc('Prices')
loc_data['prices_sharing_loc'] = get_manual_homeloc('Prices Sharing')
loc_data['prices_export_loc'] = get_manual_homeloc('Prices Export')
loc_data['prices_getall_loc'] = get_manual_homeloc('Price Getall')
loc_data['prices_getlast_week_loc'] = get_manual_homeloc('Price Get Las week')
loc_data['prices_export_conf_loc'] = get_manual_homeloc('Prices Export Confirm')
loc_data['port_add_to_port_loc'] = get_manual_homeloc('add_to_port_loc')
loc_data['port_add_muilt_loc'] = get_manual_homeloc('add_muilt_loc ')
loc_data['port_lookup_loc'] = get_manual_homeloc('Lookup Shares')
loc_data['port_confirm_loc'] = get_manual_homeloc('Add Shares Confirm')
loc_data['first_item'] = get_manual_homeloc('First Item ')
loc_data['port_delete_all'] = get_manual_homeloc('Delete All')
loc_data['screen_divider_loc'] = get_manual_homeloc('Screen Divider Location')


with open(screen_config_pickle, 'wb') as handle:
    pickle.dump(loc_data, handle, protocol=pickle.HIGHEST_PROTOCOL)



