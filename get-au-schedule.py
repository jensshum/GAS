from ctypes import WinError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import time
from datetime import timedelta
import datetime
import os

#GLOBAL VARIABLES---------------------------------------------------------------------------------

now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%m/%d/%Y')
VISIT_TYPE = "Ant"
date_to_use = TODAYS_DATE.replace("/","_")
#Driver Variables
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#-------------------------------------------------------------------------------------------------

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search
def wait_until_available(search_term, qualifier, item):
    try_count = 1
    while try_count < 30:
        try: 
            if qualifier == "ID":
                if item == "click":
                    search_by_ID(search_term).click()
                elif item == "clear":
                    search_by_ID(search_term).clear()
                else:
                    search_by_ID(search_term).send_keys(item)
                
            elif qualifier == "XPATH":
                if item != "click":
                    search_by_XPATH(search_term).send_keys(item)
                elif item == "click":
                    search_by_XPATH(search_term).click()
            break
        except Exception as e:
            print(f"Error: {e}, Retrying...")
            sleep(.5)
            try_count += 1

def latest_download_file():
    path = 'C:/Users/owner/Downloads'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]

    return newest

def main():
    
    driver.get("https://azafurapp.ecwcloud.com/mobiledoc/jsp/webemr/login/newLogin.jsp#/mobiledoc/jsp/webemr/jellybean/labs/[…]anL-Lab-DI-Procedure-ListView.jsp/lab")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "doctorID")))
    wait_until_available("doctorID", "ID", "cadymaier")
    wait_until_available("nextStep", "ID", "click")
    wait_until_available("passwordField", "ID", "Urology1!")
    wait_until_available("Login", "ID", "click")
    wait_until_available("jellybean-panelLink4", "ID", "click")
    wait_until_available('//div[@id="leftnavApp"]/nav/ul/li[4]', "XPATH", "click")
    wait_until_available('//div[@id="leftnavApp"]/nav/ul/li[4]/div/div/ul/li[2]', "XPATH", "click")
    wait_until_available('//div[@id="registry"]/div[3]/div/div/div/div/div/nav/ul/li[10]', "XPATH", "click")
    wait_until_available("EncDateFrom", "ID", "clear")
    wait_until_available("EncDateFrom", "ID", TODAYS_DATE)
    wait_until_available("EncDateTo", "ID", "clear")
    wait_until_available("EncDateTo", "ID", TODAYS_DATE)
    wait_until_available("visitTypeCombo", "ID", VISIT_TYPE)
    wait_until_available("registryBtn1", "ID", "click")
    wait_until_available("registryBtn6", "ID", "click")
    wait_until_available("registryLink10", "ID", "click")

    fileends = "crdownload"
    while "crdownload" == fileends:
        sleep(.5)
        newest_file = latest_download_file()
        if "crdownload" in newest_file:
            fileends = "crdownload"
        else:
            sleep(2)
            try_count = 0
            while try_count < 5:
                print(newest_file)
                try:
                    print(newest_file)
                    os.rename("C:/Users/owner/Downloads/" + newest_file, "C:/Users/Owner/Documents/GAS/au-schedules/au_{}.csv".format(date_to_use))
                    break
                except Exception as e:
                    print('not written', e)
                    sleep(1)
                    try_count += 1
                except WinError: 
                    break
            sleep(2)
            fileends = "none"


    driver.quit()
    
if __name__ == "__main__":
    main()
