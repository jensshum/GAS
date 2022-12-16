from logging import root
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import urllib.request
import psycopg2
from time import sleep
from datetime import date, timedelta
import datetime
import pandas as pd
import os
import pyautogui as py


now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%Y-%m-%d')
date_to_use = YESTERDAYS_DATE
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
file_to_use = 'C:/Users/Owner/Documents/GAS/forest_canyon_patients/forest_canyon_patient_names_{}.txt'.format(date_to_use.replace('/','_'))

# FUNCTION -------------------------------------------------------------------------------------------------------------

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search

def wait_until_available(search_term, qualifier, item):
    try_count = 1
    while try_count < 20:
        try: 
            if qualifier == "ID":
                if item == "click":
                    search_by_ID(search_term).click()
                elif item == "clear":
                    search_by_ID(search_term).clear()
                else:
                    search_by_ID(search_term).send_keys(item)
                
            elif qualifier == "XPATH":
                if item == "click":
                    search_by_XPATH(search_term).click()
                elif item == "clear":
                    search_by_XPATH(search_term).clear()
                else:
                    search_by_XPATH(search_term).send_keys(item)
            break
        except Exception as e:
            print(f"Error: {e}, Retrying...")
            sleep(.5)
            try_count += 1

def patient_names_to_write():
    with open(file_to_use,'r') as f:
        names = f.read().split('\n')
    return names

def input_patient_names():
    patient_names = patient_names_to_write()
    wait_until_available('//body/div[4]/button','XPATH','click')
    for name in patient_names:
        wait_until_available('/html/body/nav/div/div[1]/div/sis-patient-search/p-autocomplete/span/input','XPATH', 'clear')
        wait_until_available('/html/body/nav/div/div[1]/div/sis-patient-search/p-autocomplete/span/input','XPATH', name)
        wait_until_available('//*[@id="pr_id_1_list"]/li/sis-patient-search-result','XPATH', 'click')
        # sleep(10)
        
        # driver.execute_script('''var targLink = document.querySelector('#cdetails_attach_icon');
        #                          var clickEvent = document.createEvent('MouseEvents');
        #                          clickEvent.initEvent('ng-click', true, true);
        #                          targLink.dispatchEvent(clickEvent);''')
        try_count = 0
        while try_count < 10:
            try:
                search_by_XPATH('//*[@id="cdetails_attach_icon"]').click()
                break
            except Exception:
                try:
                    element = search_by_XPATH('//*[@id="cdetails_attach_icon"]')
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    element.click()
                    break
                except Exception:
                    sleep(1)
                    try_count += 1


        wait_until_available('/html/body/div[2]/div/div[2]/ul/li/ng-include/div/div[2]/accordion/div/div[7]/div[1]/h4/a/div/div','XPATH', 'click')
        try:
            if search_by_XPATH('/html/body/div[2]/div/div[2]/ul/li/ng-include/div/div[2]/accordion/div/div[7]/div[1]/h4/a/div/div/div[1]/i').get_attribute('class') == 'fa fa-check-circle ng-scope':
                print('trueee')
        except Exception:
            pass
        
        sleep(10)
        wait_until_available('//*[@id="pcp_print_icon1"]','XPATH', 'click')
        wait_until_available('/html/body/div[4]/div/div/div/div[2]/ul/li[2]','XPATH', 'click')
        wait_until_available('/html/body/div[4]/div/div/div/div[3]/div/button[2]/span[2]','XPATH', 'click')
        sleep(2)
        wait_until_available('/html/body/div[4]/div/div/div/div[3]/div/button','XPATH', 'click')
        sleep(5)
        for i in range(9):
            py.press('tab')
        py.press('enter')
        sleep(2)
        py.write(name.upper().replace(", ","_") + "_FC_CBO_DOWNLOAD.pdf")
        py.press('enter')
        sleep(3)
        wait_until_available('/html/body/div[4]/div/div/div/div[1]/h2/button','XPATH', 'click')
        sleep(3)


# MAIN ---------------------------------------------------------------------------------------------------------------

def main():

    driver.get("https://forestcanyon.amkaicloud.com/login.html")
    search_by_XPATH('//*[@id="username"]').send_keys('cvaltierra')
    search_by_XPATH('//*[@id="password"]').send_keys('Sunflower4!')
    search_by_XPATH('//*[@id="LoginButton"]').click()
    wait_until_available('//*[@id="gem-orgs"]/div[2]','XPATH','click')
    input_patient_names()

if __name__ == "__main__":
    main()