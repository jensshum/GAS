from encodings import search_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import date, timedelta
import datetime
import pandas as pd
import os
import pyautogui as py

# GLOBALS --------------------------------------------------------------------------------

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%m/%d/%Y')

# FUNCTIONS ------------------------------------------------------------------------------

def search_by_ID(id_code):
    try_count = 0
    while try_count < 15:
        try:
            search = driver.find_element(By.ID, id_code)
            return search
        except Exception:
            print("Error.")
            try_count += 1
            sleep(.5)

def search_by_XPATH(Xpath):
    try_count = 0
    while try_count < 15:
        try:
            search = driver.find_element(By.XPATH, Xpath)
            return search
        except Exception:
            print("Error.")
            try_count += 1
            sleep(.5)

def latest_download_file():
    path = 'C:/Users/Owner/Downloads'
    os.chdir(path)
    sleep(1)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest

# MAIN ------------------------------------------------------------------------------------

def main():
    driver.get("https://gans.epreop.com/OfficeAdmin/clientLogin.aspx")
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName"]').send_keys('shshumway')
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password"]').send_keys('Gofastgas22')
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_btnSubmit"]').click()
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_divReports"]/div/div').click()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_dlReports"]/tbody/tr[6]/td[2]/div[2]/span/span').click()
    search_by_XPATH('//*[@id="ProcedureStartDate"]').send_keys(YESTERDAYS_DATE)
    search_by_XPATH('//*[@id="ProcedureEndDate"]').send_keys(YESTERDAYS_DATE)
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_btnRunReport"]').click()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_ButtonLink"]').click()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_Menu"]/div[5]/a').click()
    #DATAPORTAL 
    driver.get("https://dataportal.greatergas.com/")
    search_by_XPATH('//*[@id="inputUsername"]').send_keys('sheldon')
    search_by_XPATH('//*[@id="inputPassword"]').send_keys('Gofastgas22')
    search_by_XPATH('//*[@id="layoutAuthentication_content"]/main/div/div/div/div/div[2]/form/button').click()
    driver.get("https://dataportal.greatergas.com/automation-step1")
    
    fileends = "crdownload"

    while "crdownload" == fileends:
        sleep(.5)
        newest_file = latest_download_file()
        print(newest_file)
        if "crdownload" in newest_file:
            fileends = "crdownload"
        else:
            break
    sleep(2)
    try_count = 0
    while try_count < 5:
        try:
            search_by_XPATH('//*[@id="myFile"]').send_keys("C:/Users/noahs/Downloads/" + str(newest_file))
            break
        except Exception:
            sleep(1)
            try_count += 1
    search_by_XPATH('//*[@id="btnFetch"]').click()
                    
    


if __name__ == "__main__":
    main()