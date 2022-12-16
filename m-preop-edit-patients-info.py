from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import username, password
from selenium.webdriver.support.ui import Select
import pyautogui as py
import sys
import psycopg2
from time import sleep
import time



#GLOABALS--------------------------------------------------------------------------------------------------
URL = 'https://m.epreop.com/Account/Login'
chrome_options = Options()
# chrome_options.add_argument("--headless")
# if len(sys.argv) > 1:
#     if len(sys.argv) < 5:
#         START_ITEM = int(sys.argv[1])
# else:
START_ITEM = 0

conn = psycopg2.connect(
    host="cbo-mirror.cbo8fr4pmlfg.us-east-2.rds.amazonaws.com",
    port = "5432",
    user="postgres",
    password= "gr8ergas",
    sslmode="require",
    sslrootcert="SSLCERTIFICATE")

cur = conn.cursor()

#FUNCTIONS -----------------------------------------------------------------------------------------------
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH,options=chrome_options)

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
                elif item == "RETURN":
                    search_by_ID(search_term).send_keys(Keys.RETURN)
                else:
                    search_by_ID(search_term).send_keys(item)

            elif qualifier == "XPATH":
                if item == "click":
                    search_by_XPATH(search_term).click()
                    # break
                elif item == "clear":
                    search_by_ID(search_term).clear()
                else:
                    search_by_XPATH(search_term).send_keys(item)

            elif qualifier == "CLASS_NAME":
                if item == "click":
                    search = driver.find_element(By.CLASS_NAME, search_term)
                    search.click()
                elif item == "clear":
                    search = driver.find_element(By.CLASS_NAME, search_term)
                    search.clear()
                else:
                    search = driver.find_element(By.CLASS_NAME, search_term)
                    search.send_keys(item)
            break
        except Exception as e:
            if try_count == 1:
                print(f"Error, Retrying...")
            else:
                print(f"Error, retrying... try count: {try_count}")
            sleep(.5)
            try_count += 1

def get_undedited_patients():
    unedited_records_query = '''SELECT * FROM uneditedrecords WHERE corrected <> 'true'; '''
    cur.execute(unedited_records_query)
    unedited = cur.fetchall()
    # print(unedited)
    return unedited

def get_patient_to_edit(number):
    records_to_edit_query = '''SELECT * FROM recordsedited WHERE epreop_number = '{}'; '''.format(number)
    cur.execute(records_to_edit_query)
    data_to_edit = cur.fetchone()
    # print("DATATOEDIT",data_to_edit)

    return data_to_edit

def set_date():
    wait_until_available('//*[@id="mainContent"]/form/div[2]/h3/a','XPATH','click')
    select = Select(driver.find_element(By.ID, 'Search_ProcedureDateId'))
    select.select_by_value(',')
    wait_until_available('btnSearchList','ID','click')

def return_lowercase(patient,qualifier):
    if qualifier == 'firstname':
        first_name = patient.split(",")[1]
        first_name = first_name[0] + first_name[1:].lower()
        return first_name
    elif qualifier == 'lastname':
        last_name = patient.split(",")[0]
        last_name = last_name[0] + last_name[1:].lower()
        return last_name

def return_formatted_date(date):
    if len(date) > 10:
        date = date.split(" ")[0].split("-")
        date = date[1] + "/" + date[2] + "/" + date[0]
        return date
    else:
        date = date.split("-")
        date = date[1] + "/" + date[2] + "/" + date[0]
        return date

def update_postgre(name,number):
    first_name = name.split(',')[1]
    last_name = name.split(',')[0]
    records_edited_query = '''UPDATE recordsedited SET corrected = 'true' WHERE patient_firstname = '{}' AND patient_lastname = '{}' '''.format(first_name,last_name)
    unedited_records_query = '''UPDATE uneditedrecords SET corrected = 'true' WHERE epreop_number = '{}';'''.format(number)
    print('Database updated.')
    cur.execute(records_edited_query)
    cur.execute(unedited_records_query)
    conn.commit()

def edit_patient_info(START_ITEM=0):
    date_set = False
    to_edit = get_undedited_patients()
    if len(str(START_ITEM)) > 5:
        for i in range(len(to_edit)):
            if str(START_ITEM) == str(to_edit[i][7]).replace(".0",""):
                START_ITEM = i
    for i in range(START_ITEM,len(to_edit)):
        unedited_patient_name = str(to_edit[i][4]) + "," + str(to_edit[i][5])
        print(unedited_patient_name)
        epreop_number = str(to_edit[i][8]).replace(".0","")
        print(epreop_number)
        try:
            patient_data = get_patient_to_edit(epreop_number)
            patient_name = patient_data[3] + "," + patient_data[4]
            dob = str(patient_data[5])
            dos = str(patient_data[19])
        except TypeError:
            continue
        print(f"Starting new search. Patient Name: {unedited_patient_name} ")
        wait_until_available('Search_PatientName','ID','clear')
        wait_until_available('Search_PatientName','ID',unedited_patient_name)
        # sleep(10)
        if date_set == False:
           set_date()
        date_set = True
        wait_until_available('Search_PatientName','ID','RETURN')
        sleep(5)
        if len(driver.find_elements(By.XPATH,'//*[@id="mainContent"]/form/ul/li')) == 0:
            print('No record found. Moving on to next record.')
            update_postgre(patient_name,epreop_number)
            continue
        else:
            print('Record found. Making edits.')
            wait_until_available('//*[@id="mainContent"]/form/ul/li[1]','XPATH','click')
            try_count = 0
            next_option = True
            while try_count < 6:
                try:
                    search_by_XPATH('//*[@id="patientDetails"]/div[1]/div/a').click()
                    next_option = False
                except:
                    sleep(.5)
                    try_count += 1
            if next_option == True:
                wait_until_available('//*[@id="patientDetails"]/div[2]/div/a','XPATH','click')
            # wait_until_available('//*[@id="patientDetails"]/div[1]/div/a','XPATH','click')
            wait_until_available('PatientFirstName','ID','clear')
            wait_until_available('PatientLastName','ID','clear')
            wait_until_available('PatientFirstName','ID', return_lowercase(patient_name,'firstname'))
            wait_until_available('PatientLastName','ID', return_lowercase(patient_name,'lastname'))
            wait_until_available('DOB_DatePicker','ID', 'clear')
            wait_until_available('DOB_DatePicker','ID', return_formatted_date(dob))
            wait_until_available('ProcedureDate_DatePicker','ID', 'clear')
            wait_until_available('ProcedureDate_DatePicker','ID', return_formatted_date(dos))
            wait_until_available('//*[@id="mainContent"]/div[1]/form/div[14]/button','XPATH', 'click')
            print(patient_name, epreop_number)
            update_postgre(patient_name,epreop_number)
            print('Record updated. Back to Menu.')
            wait_until_available('//*[@id="Header_Menu"]','XPATH', 'click')
            wait_until_available('//*[@id="Header_HomeButton"]','XPATH', 'click')

# MAIN -------------------------------------------------------------------------------------------------------
def main():
    start = time.time()
    patient_len = len(get_undedited_patients())
    print(patient_len)
    if patient_len == 0:
        pass
    else:
        driver.get(URL)
        driver.find_element(By.ID,"UserName").send_keys("shshumway")
        driver.find_element(By.ID,"UserPassword").send_keys("Gofastgas22")
        driver.find_element(By.NAME,"SiteURLToken").send_keys("GANS")
        driver.find_element(By.ID,"btnlogin").click()
        wait_until_available('//*[@id="pre-rendered-page"]/div[2]/ul/li[2]/a','XPATH','click')
        edit_patient_info(START_ITEM)
    end = time.time()
    elapsed_time = end-start
    print("elapsed time in seconds: ", elapsed_time)
    print("Completed Script.")
    cur.close()
    conn.close()
    driver.quit()



if __name__ == "__main__":
    main()
