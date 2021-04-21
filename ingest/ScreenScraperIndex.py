from ingest.scraper_helpers import *
import pyautogui
from pyautogui import Point
from time import sleep

y_gap = 25
no_tics_per_page = 20


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

first_item_loc = Point(x=76, y=356)
last_item_loc = Point(x=730, y=932)

price_share_loc = Point(x=1310, y=207);
price_export_loc= Point(x=1305, y=270)

sleep(5)
for i in range(0,46):
    pyautogui.click(first_item_loc)#, duration=0.15, tween=pyautogui.easeInOutQuad)
    sleep(0.15)
    pyautogui.scroll(-50)
    pyautogui.click(first_item_loc)
    sleep(0.25)
    pyautogui.moveTo(price_share_loc)
    sleep(0.25)
    pyautogui.click(price_share_loc)
    sleep(0.25)
    pyautogui.moveTo(price_export_loc)
    sleep(0.25)
    pyautogui.click(price_export_loc)


xppos = 730;
ypos=925;
delta = 25;
sleep(2)
pyautogui.click(last_item_loc)  # , duration=0.15, tween=pyautogui.easeInOutQuad)
for i in range(0, 25):
    sleep(0.25)
    loc = (xppos,ypos);
    pyautogui.click(loc)
    sleep(0.25)
    pyautogui.click(price_share_loc)
    sleep(0.25)
    pyautogui.moveTo(price_export_loc)
    sleep(0.25)
    pyautogui.click(price_export_loc)
    ypos-=25;


