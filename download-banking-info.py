from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from time import sleep
from datetime import timedelta
import datetime
import os

#%% OPEN PROVATION
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

NOW = datetime.datetime.now()
TODAY = NOW.strftime('%m/%d/%Y')
TOMORROW = NOW + timedelta(days = 1)
YESTERDAY = NOW - timedelta(days = 1)
YESTERDAYS_DATE = YESTERDAY.strftime('%m/&d/%Y')
folder_name = NOW.strftime('%m %d') + " DOWNLOAD DOS " + YESTERDAY.strftime('%m %d') + " CASES"
# folder_name = "08 02" + " DOWNLOAD DOS " + "08 01" + " CASES"
TOMORROW_DATE = TOMORROW.strftime('%m/%d/%Y')
today = NOW.strftime('%m %d')

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

def findNewestFile():
    path = "C:/Users/noahs/Downloads"
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    print("Newest file: ", newest)
    return path + "/" + str(newest)


# MAIN -------------------------------------------------------------------------
def main():
    #%% LOGIN TO QUICKBOOKS
    driver.get("https://app.qbo.intuit.com/app/login?loadCustomerAssistanceAssets=us&product=qbOnline")
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ius-signin-userId-input"))
        )
    except:
        driver.quit()

    search_by_ID("ius-signin-userId-input").send_keys("sheldon@greatergas.com")
    search_by_ID("ius-identifier-first-submit-btn").click()
    search_by_ID("iux-password-confirmation-password").send_keys("Gofastgas22!")
    search_by_XPATH('//*[@id="ius-sign-in-mfa-parent"]/div/form/button[2]').click()
    sleep(5)
    driver.get("https://app.qbo.intuit.com/app/register?accountId=234")
    search_by_XPATH('//*[@id="uniqName_8_0"]').clear()
    search_by_XPATH('//*[@id="uniqName_8_0"]').send_keys('FIB RCM Deposits 5759')
    search_by_XPATH('//*[@id="uniqName_8_0"]').send_keys(Keys.RETURN)
    sleep(1)
    search_by_XPATH('//*[@id="dijit_form_DropDownButton_0"]').click()
    search_by_XPATH('//*[@id="uniqName_11_2"]').send_keys(NOW.strftime('%m/01/%Y'))
    search_by_XPATH('//*[@id="uniqName_11_3"]').send_keys(TODAY)
    search_by_XPATH('//*[@id="uniqName_54_0"]/div[1]/div/div/div[2]/button').click()
    search_by_XPATH('//*[@id="uniqName_1_1"]/i[4]').click()
    sleep(3)
    driver.get('https://dataportal.greatergas.com')
    search_by_ID('inputUsername').send_keys("sheldon")
    search_by_ID('inputPassword').send_keys('Gofastgas22')
    search_by_ID('inputPassword').send_keys(Keys.RETURN)

    driver.get('https://dataportal.greatergas.com/pb_qbdata')
    sleep(3)
    search_by_ID('myFile').send_keys(findNewestFile())
    sleep(2)
    search_by_ID('uploadbtn').submit()

if __name__ == "__main__":
    main()

#%% DOWNLOAD BANKING INFO
