from pywinauto.application import Application as ap
import pyautogui as py
from datetime import date, timedelta
import datetime
from time import sleep
import os

#GLOBAL--------------------------------------------------------------------------------------------

NOW = datetime.datetime.now()
TODAY = NOW.strftime('%m/%d/%Y')
TOMORROW = NOW + timedelta(days = 1)
YESTERDAY = NOW - timedelta(days = 1)
YESTERDAYS_DATE = YESTERDAY.strftime('%m/%d/%Y')
TOMORROW_DATE = TOMORROW.strftime('%m/%d/%Y')
today = NOW.strftime('%m %d')

date_to_use = YESTERDAYS_DATE

tm = u"\u2122"
app_title = "AmkaiOffice" + tm + " 4.5.1 [ cvaltierra ]"

# MAIN ----------------------------------------------------------------------------------------

# def main():
#     sleep(1)
#     py.click(x=68, y=117)
#     sleep(3)
#     py.click(1476, 150)
#     sleep(2)
#     py.click(x=46, y=330)
#     sleep(10)
#     py.click(x=462, y=165)
#     sleep(1)
#     py.press('tab')
#     py.write(date_to_use)
#     py.press('tab')
#     py.write(date_to_use)
#     py.click(x=1332, y=260)
#     py.click(x=449, y=636)
#     py.keyDown('shift')
#     py.click(x=425, y=675)
#     py.keyUp('shift')
#     py.click(x=1472, y=906)
#     sleep(1)
#     py.click(x=1077, y=652)
#     sleep(7)
#     py.click(x=235, y=185)
#     sleep(9)
#     py.click(x=959, y=878)
#     sleep(20)
#     py.write("FOREST_CANYON_CBO_DOWNLOAD_" + date_to_use.replace("/","-"))
#     py.press('enter')
    
# if __name__ == "__main__":
#     main()
def main():
    sleep(1)
    py.click(x=50, y=75)
    sleep(3)
    py.click(x=1480, y=156)
    sleep(2)
    py.click(x=48, y=294)
    sleep(10)
    py.click(x=516, y=126)
    sleep(1)
    py.press('tab')
    py.write(date_to_use)
    py.press('tab')
    py.write(date_to_use)
    py.click(x=1304, y=242)
    py.click(x=453, y=658)
    py.keyDown('shift')
    py.click(x=468, y=697)
    py.keyUp('shift')
    py.click(x=1441, y=927)
    sleep(1)
    py.click(x=1053, y=642)
    sleep(7)
    py.click(x=233, y=135)
    sleep(9)
    py.click(x=950, y=827)
    sleep(20)
    py.write("FOREST_CANYON_CBO_DOWNLOAD_" + date_to_use.replace("/","-"))
    py.press('enter')
    
if __name__ == "__main__":
    main()
