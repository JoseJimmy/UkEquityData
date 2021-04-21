import pickle
import pandas as pd
from datetime import datetime

from Input.scraper_helpers import *
from processing.UpdateTracker import update_tracker_csv
from settings import *
from datetime import datetime, timedelta
import winsound
import math
import pyautogui
from pyautogui import Point
from time import sleep
from time import sleep
import pandas as pd
import tkinter as tk
import pickle
import pyperclip  # handy cross-platform clipboard text handler
import time

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


def copy_clipboard():
    time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
    return pyperclip.paste()

sleep(5)
first_item=(76, 357)
locs = {'summary_loc': pyautogui.Point(x=1003, y=206),
        'company_loc': Point(x=1069, y=205),
        'window_body': Point(x=1628, y=460),
        'Drag_start': Point(x=1592, y=999),
        'Drag_end': Point(x=969, y=255),
        'end_scroll_loc' : Point(1910, 979)}


pyautogui.click(first_item, duration=0.15, tween=pyautogui.easeInOutQuad)
summary_loc = locs['summary_loc']
window_body = locs['window_body']

company_loc = locs['company_loc']
Drag_start = locs['Drag_start']
Drag_end = locs['Drag_end']
end_scroll_loc = locs['end_scroll_loc']
sleep(5)
for i in range(0,20,1):
    pyautogui.click(first_item)#, duration=0.15, tween=pyautogui.easeInOutQuad)
    sleep(0.25)
    pyautogui.moveTo(summary_loc)#, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.click(summary_loc)
    pyautogui.moveTo(company_loc)#, duration=0.15, tween=pyautogui.easeInOutQuad)
    pyautogui.click(company_loc)


    # pyautogui.click(Drag_start)
    # pyautogui.mouseDown()  # press the left button down
    # pyautogui.moveTo(Drag_end)#, duration=1, tween=pyautogui.easeInOutQuad)
    # sleep(0.75)
    # pyautogui.mouseUp()

    pyautogui.click((window_body))
    sleep(1)
    pyautogui.scroll(-2500)
    sleep(1)
    # pyautogui.mouseDown()  # press the left button down
    # sleep(0.5);

    pyautogui.moveTo((Drag_start))
    sleep(1)

    pyautogui.mouseDown()  # press the left button down
    sleep(0.2)

    pyautogui.moveTo((Drag_end))
    sleep(1)
    pyautogui.mouseUp()

    var = copy_clipboard()
    ctime_str = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    filename = r"C:\PythonProjects\ShrPadDataProcs\Input\temp\item_%s_%s.txt" % (i,ctime_str)
    with open(filename,"a",encoding='UTF-8') as myfile:
        myfile.write(var)
    pyautogui.moveTo(first_item)
    pyautogui.scroll(-18)
    sleep(0.5)
# os.system('shutdown /s /f ')

#
#
# import pandas as pd
# import os
# def getFileNames(dir, filt_key='.', ext='.csv'):
#     Files = []
#     for file in os.listdir(dir):
#         if file.endswith(ext):
#             if file.lower().count(filt_key.lower()) > 0:
#                 Files.append(os.path.join(dir, file))
#     return Files
#
tic_list = []
summary = {}
files = getFileNames('Input/temp/','.','.txt')
for idx,file in enumerate(files) :
    with open(file,'r',encoding= ' UTF-8') as f:
        lines = f.read()
    if lines.find('SUMMARY') > 0  :
        summ = lines.split('SUMMARY')[1].split('DIRECT')[0].strip()
        ticker = lines.split('KEY INFORMATION')[1].split('ISIN')[0].split('TIDM')[1].strip()
        summary[ticker] = summ
        # print(summ, 5*'\n\n')
        tic_list.append(ticker.split(':')[1])
tracker = pd.read_csv(scrape_list_csv, parse_dates=['Price_start', 'Price_end', 'Price_downloaded'])
x = pd.DataFrame(list(set(tracker.Ticker) - set(tic_list)))
summary_df = pd.DataFrame.from_dict(summary,orient='index')
summary_df.to_csv(r'c:\data\ref\summary.csv')
#

#     if lines.find('SUMMARY') >0  :


#
# tic_list = []
# summary = {}
# files = getFileNames('Input/temp/','.','.txt')
# for idx,file in enumerate(files) :
#     with open(file,'r',encoding= ' UTF-8') as f:
#         lines = f.read()
#     if(lines.find('No breakdownavailable') == -1)
#         print(lines.split('Region	Turnover')[1].split('Product	Turnover')[0].replace('\n\n','\n'))/