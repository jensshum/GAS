from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import psycopg2
from time import sleep
from datetime import date, timedelta
import datetime
import pandas as pd
import os

now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%#m/%#d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%Y-%m-%d')
date_to_use = now.strftime('%m_%d_%Y')
PATH = "C:\Program Files (x86)\msedgedriver.exe"
driver = webdriver.Edge(PATH)

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.ID, Xpath)
    return search


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://gans.epreop.com/OfficeAdmin/clientLogin.aspx")

file = "C:/Users/owner/Documents/GAS/au-schedules/au_{}.csv".format(TODAYS_DATE.replace("/","_"))

with open(file, 'r') as file:
    df = pd.read_csv(file)


#%% LOGIN EPREOP
try: 
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName"))
    )
except:
    driver.quit()
search = driver.find_element(By.ID,"ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName")
search.send_keys("shshumway")
search2 = driver.find_element(By.ID,"ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password")
search2.send_keys("Gofastgas22")
search2.send_keys(Keys.RETURN)
while len(driver.find_elements(By.ID,"RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane")) == 0:
    sleep(.5)
    print("slept for frame")

#%% ENTER ADD PATIENT
try:
    Xpath = '''//div[@onclick="javascript:window.parent.showLoader();reDirectTo('/OfficeAdmin/Patient/patientDetail.aspx?mode=new')"]'''
    search = driver.switch_to.frame("RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane")
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, Xpath))
    )
    while len(driver.find_elements(By.XPATH, Xpath)) == 0:
        sleep(.5)
        print("Slept for Patient search")
    search = driver.find_element(By.XPATH, Xpath)
    print('path found')
except Exception as e:
    print(f"Could not locate element: {e}")
    driver.close()
print("Entered Add New Patient")
search.click()

numrows = df.shape[0]
print("Columns: ", df.columns)
for i in range(numrows):
   
    mrn = df.iloc[i]['Acc #']
    patient_name = df.iloc[i]['Patient Name']
    split = patient_name.split(",")
    last_name = split[0]
    first_name = split[1]
    
    date_of_birth = df.iloc[i]['DOB']
    substr = date_of_birth.split("/")
    month = substr[0]
    day = substr[1]
    year = substr[2]
    if month == '1' or month == '01':
        month = 'Jan'
    elif month == '2' or month == '02':
        month = "Feb"
    elif month == '3' or month == '03':
        month = "Mar"
    elif month == '4' or month == '04':
        month = "Apr"
    elif month == '5' or month == '05':
        month = "May"
    elif month == '6' or month == '06':
        month = "Jun"
    elif month == '7' or month == '07':
        month = "Jul"
    elif month == "8" or month == '08':
        month = "Aug"
    elif month == "9" or month == '09':
        month = "Sep"
    elif month == "10":
        month = "Oct"
    elif month == "11":
        month = "Nov"
    elif month == "12":
        month = "Dec"
    print("this is the month", month)
    print("this is the day", day)
    if day[0] == '0':
        day = day.replace("0","")
    gender = df.iloc[i]['Sex']
    phone = df.iloc[i]['Tel. No.']
    facility = 'Affilitated Urologists'
    while len(driver.find_elements(By.ID, "ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtMRN")) == 0:
        sleep(.5)
        print('slept for patient search')
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtMRN").clear()
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtMRN").send_keys(str(mrn))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtLastName").clear()
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtLastName").send_keys(str(last_name))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtFirstName").clear()
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtFirstName").send_keys(str(first_name))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_DOB_ddlMonth").send_keys(str(month))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_DOB_ddlDay").send_keys(day)
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_DOB_ddlYear").send_keys(year)
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_cboGender").send_keys(str(gender))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtPhone").clear()
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtPhone").send_keys(str(phone))
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtPatientAddress").clear()
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtNewPatientMedicalProcedureName").clear()
   
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtProcedureDate").clear()
    vardate = TODAYS_DATE
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_txtProcedureDate").send_keys(vardate)
    
    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_ddlClientFacilities1").send_keys(str(facility))
    search_by_ID("btnAddProvider").click()
    select = Select(driver.find_element(By.XPATH, '//div[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_pnlProviders"]/table/tbody/tr/td/table/tbody/tr/td[1]/select'))
    select.select_by_value("de8b793f-5750-4b40-8ed4-091a492aa3ee")
    
    #%% DATE FINDER 
    curr_month = now.strftime("%m_%Y")
    file = 'C:/users/owner/documents/gas/IntrigmaChiefNames_for_month_{}.csv'.format(curr_month)
    df = pd.DataFrame(pd.read_csv(file))
    date_today = now.strftime('%b %#d')
    for i in range(df.shape[0]):
        thing = str(df.loc[i][1])
        split = thing.split("\n")
        date = split[0]
        if date_today == date:
            anes_provider = split[4].replace(".","")
            print(split[4].replace(".",""))

    
    select = Select(driver.find_element(By.XPATH, '''//div[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_pnlProviders"]/table/tbody/tr/td/table/tbody/tr/td[3]/select'''))
    
    if "Alexander" in anes_provider:
        select.select_by_value("c0c9a6b8-45fd-4d1b-b3d9-f33517223a95")
    elif "Moore" in anes_provider:
        select.select_by_value("4b521c9a-0631-ec11-9023-0022488db7b8")
    elif "Jimenez" in anes_provider:
        select.select_by_value("81ee96b4-081d-4f6a-a2c8-5d9116df6abd")
    elif "Smith" in anes_provider:
        select.select_by_value("f9704d1f-57e9-4d86-a52b-b4b3c15ba136")

    search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_btnSave").click()
    sleep(4)
    driver.execute_script("window.history.go(-1)")








