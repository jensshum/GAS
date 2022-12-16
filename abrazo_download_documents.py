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

# GLOBALS ------------------------------------------------------------------------

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://login.etenet.com/app/UserHome")

now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%m/%d/%Y')

def search_by_ID(id_code):
    try_count = 0
    while try_count < 10:
        try:
            search = driver.find_element(By.ID, id_code)
            return search
        except Exception:
            print("Error.")
            try_count += 1
            sleep(.5)

def search_by_XPATH(Xpath):
    try_count = 0
    while try_count < 10:
        try:
            search = driver.find_element(By.XPATH, Xpath)
            return search
        except Exception:
            print("Error.")
            try_count += 1
            sleep(.5)
        
def return_patient_names():
    
    with open('C:/Users/Owner/Documents/GAS/ABRAZO_PATIENTS/abrazo_arrowhead_patient_list_{}.txt'.format(YESTERDAYS_DATE.replace("/","_")),'r') as f:
        content = f.read()
        names = content.split('\n')
    
    return names




# MAIN ---------------------------------------------------------------------

def main():
    search_by_XPATH('//*[@id="okta-signin-username"]').send_keys('karen.paterno')
    search_by_XPATH('//*[@id="okta-signin-password"]').send_keys('Rathbun15##')
    search_by_XPATH('//*[@id="okta-signin-password"]').send_keys(Keys.RETURN)
    sleep(10)
    for i in range(3):
        py.keyDown('ctrl')
        py.press('w')
        py.keyUp('ctrl')
    sleep(1)
    search_by_XPATH('//*[@id="main-content"]/section/section[1]/section/div[1]/a').click()
    sleep(3)
    py.write('Rathbun15##')
    py.press('enter')
    sleep(3)
    # py.press('tab')
    # py.press('enter')
    sleep(9)
    driver.get("https://physicianportal.etenet.com/PhysicianPortal/Default.aspx")
    py.keyDown('ctrl')
    py.press('w')
    py.keyUp('ctrl')
    sleep(2)
    select = Select(driver.find_element(By.XPATH, '//*[@id="FacilityDropDownList"]'))
    select.select_by_value('AHD')
    search_by_XPATH('//*[@id="TabsMenun1"]/table/tbody/tr/td/a/div/div[2]').click()
    driver.switch_to.frame('TabContentIFrame')
    search_by_XPATH('//*[@id="FunctionalAreaNavigator_FunctionalAreaMenun1"]/table/tbody/tr/td/a').click()
    patients = return_patient_names()
    for patient in patients:
        
        if "MRN" in patient:
            continue
        driver.switch_to.default_content()
        driver.switch_to.frame('TabContentIFrame')
        search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_MedicalRecordNumberTextBox"]').clear()
        search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_MedicalRecordNumberTextBox"]').send_keys(patient)
        search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_SearchActiveImageButton"]').click()
        # search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_Grid_patientNameLinkButton_0"]').click()
        rows = driver.find_elements(By.XPATH,'//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_Grid"]/tbody/tr')
        row_count = 1
        print(len(rows))
        for row in rows:
            if YESTERDAYS_DATE in row.text:
                print('yes')
                print(row_count)
                search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_PatientSearchTemplatedWebPartManager_gwpCensusSearch_CensusSearch_Grid"]/tbody/tr[{}]/td/a'.format(row_count)).click()
                break
            row_count += 1
        sleep(3)
        try_count = 0

        # driver.execute_script("window.history.go(-1)")

        while try_count < 5:
            try:
                print('GOTEMMMM')
                driver.switch_to.default_content()
                driver.switch_to.frame('modalWindowFrame')
                search_by_XPATH('//*[@id="ReasonCodesRadioButtonList_4"]').click()
                search_by_XPATH('//*[@id="GrantAccessButton"]').click()
                break
            except:
                print("blink 182")
                try_count += 1
                sleep(.1)
        sleep(3)
        driver.switch_to.default_content()
        driver.switch_to.frame('TabContentIFrame')
        rows = driver.find_elements(By.XPATH,'//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr')
        row_count = 1
        print(len(rows))
        for row in rows:
            print(row.text)
            if 'Operative Note' in row.text:
                print('Operative Note')
            if 'Operative Note' in row.text:
                print('yes')
                search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr[{}]/td/a'.format(row_count)).click()
                search_by_XPATH('//*[@id="WebPart_gwpTheTranscriptionResultsList"]/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr/td[3]/table/tbody/tr/td/a').click()
                print('crimwald')
                sleep(10)
                print('clumpwald')
                for i in range(2):
                    py.press('tab')
                py.press('enter')
                for i in range(10):
                    py.press('up')
                py.press('enter')
                for i in range(5):

                    py.press('tab')
                py.press('enter')
                sleep(1)
                break
            row_count += 1
        
        driver.execute_script("window.history.go(-1)")
        # sleep(2)
        # driver.execute_script("window.history.go(-1)")
        continue
    
        # sleep(2)
        # continue
        # if len(driver.find_elements(By.ID,'modalWindowFrame')) > 0:
        #     print('frame found')
        # try_count = 0
        # while try_count < 5:
        #     try:
        #         driver.switch_to.default_content()
        #         driver.switch_to.frame('modalWindowFrame')
        #         search_by_XPATH('//*[@id="ReasonCodesRadioButtonList_4"]').click()
        #         search_by_XPATH('//*[@id="GrantAccessButton"]').click()
        #         break
        #     except:
        #         print("blink 182")
        #         try_count += 1
        #         sleep(.7)

        # print("CREMMMMMLING")
        # driver.switch_to.default_content()
        # driver.switch_to.frame('TabContentIFrame')
        # rows_text = driver.find_elements(By.XPATH,'//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr/td[3]')
        # rows = driver.find_elements(By.XPATH,'//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr/td/a')
        # search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr/td[3]').text
        # # search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr/td/a').click()
        # # for row in rows:
        # #     print(row)

        # print(len(rows))
        # for row,i in enumerate(rows_text):
        #     print(row.text)
        #     if "Operative Note" in row.text:
        #         search_by_XPATH('//*[@id="FunctionalAreaContentPlaceHolder_TranscriptionWebPartManager_gwpTheTranscriptionOrdersList_TheTranscriptionOrdersList_OrdersGridView"]/tbody/tr/td/a').click()
                
        # break
    

if __name__ == "__main__":
    main()