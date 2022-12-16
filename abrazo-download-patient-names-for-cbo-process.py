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

# GLOBALS -----------------------------------------------------------------------------

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://gans.epreop.com/OfficeAdmin/clientLogin.aspx")

now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%m/%d/%Y')

# FUNCTIONS ---------------------------------------------------------------------------

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

# MAIN ---------------------------------------------------------------------------------

def main():
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName"]').send_keys('shshumway')
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password"]').send_keys('Gofastgas22')
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_btnSubmit"]').click()
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_main"]/div/div/div[2]/div').click()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput"]').clear()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput"]').send_keys(YESTERDAYS_DATE)
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcEndDate_dateInput"]').clear()
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcEndDate_dateInput"]').send_keys(YESTERDAYS_DATE)
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_ToggleAdvanceSearch"]/div').click()
    select = Select(driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_ddlSurgicalLocations"]'))
    select.select_by_value('80922ba1-269d-eb11-811a-000d3a609173')
    search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_AdvanceSearchButton"]').click()
    
    # GET PATIENT NAMES

    sleep(3)
    num_patients = search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_RadTabStripPatientSearch"]/div/ul/li[1]/a/span/span/span').text
    num_patients = int(num_patients.split("(")[1].replace(")",""))
    if num_patients > 20:
        search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00_ctl03_ctl01_PageSizeComboBox_Input"]').send_keys('100')
        search_by_XPATH('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00_ctl03_ctl01_PageSizeComboBox_Input"]').send_keys(Keys.RETURN)
        sleep(7)
    # elements = driver.find_elements(By.XPATH,'//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00"]/tbody/tr/td[2]/table/tbody/tr[1]')
    mrns = driver.find_elements(By.XPATH,'//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00"]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[2]')
    element_array = []
    # for element in elements:
    #     element_array.append(element.text)
    for mrn in mrns:
        element_array.append(mrn.text)
    with open('C:/Users/Owner/Documents/GAS/ABRAZO_PATIENTS/abrazo_arrowhead_patient_list_{}.txt'.format(YESTERDAYS_DATE.replace("/","_")),'w') as f:
        for element in element_array:
            f.write(element.replace("MRN: ",""))
            f.write("\n")
        

    

    driver.quit()
            



if __name__ == "__main__":
    main()