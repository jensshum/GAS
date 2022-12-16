from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import datetime
import pandas as pd
import os
import psycopg2
from datetime import timedelta
from selenium.webdriver.common.alert import Alert

# GLOBALS ------------------------------------------------------------------------------------------

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%m/%d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%m/%d/%Y')

# CONNECTION TO PSYCOPG2---------------------------------------------------------------------------
conn = psycopg2.connect(
    host="cbo-mirror.cbo8fr4pmlfg.us-east-2.rds.amazonaws.com",
    port = "5432",
    #database="cbo-mirror",
    user="postgres",
    password= "gr8ergas",
    sslmode="require",
    sslrootcert="SSLCERTIFICATE")

cur = conn.cursor()

# FUNCTIONS ----------------------------------------------------------------------------------------
def getNums(numsqualifier):
    clinical_review_query = "SELECT epreop_number, anes_provider FROM clinicalreview WHERE anes_provider <> '' and image_batch_id <> 'true';"
    medical_records_query = "SELECT epreop_number, anes_provider FROM medicalrecordsreview WHERE anes_provider <> '' AND corrected IS NULL OR corrected = 'false';"
    if numsqualifier == "cr":
        cur.execute(clinical_review_query)
        cr_nums = cur.fetchall()
        # for num in cr_nums:
        #     print("The nums are", num)
        return cr_nums
    elif numsqualifier == "mr":
        cur.execute(medical_records_query)
        mr_nums = cur.fetchall()
        for num in mr_nums:
            print("this is the num", num)
        return mr_nums

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search
def wait_until_available(search_term, qualifier, item ):
    try_count = 1
    while try_count < 60:
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
                print(f"Error: {e}, Retrying...")
            else:
                print(f"Error, retrying... try count: {try_count}")
            sleep(.5)
            try_count += 1
            # wait_until_available(search_term, qualifier, item, try_count)

def get_provider_name_value(provider_name):
    print("data: ", provider_name)
    options = driver.find_elements(By.XPATH, '//*[@id="providerinfo"]/tbody/tr[1]/td/table/tbody/tr[2]/td[3]/select/option')
    for option in options:
        # print(option.text)
        if provider_name in option.text.replace(",",""):
            return option.get_attribute('value')
        else:
            return

def update_postgre(epreop_num):
    query = '''UPDATE clinicalreview SET image_batch_id = 'true' WHERE epreop_number = '{}'; '''.format(epreop_num)
    cur.execute(query)
    conn.commit()

def add_clinical_review_providers():
    clinical_review_nums = getNums("cr")
    for num in clinical_review_nums:
        if str(num[0]) == '':
            continue
        driver.switch_to.default_content()
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber","ID", "clear")
        print("data", num)
        epreop_number = str(num[0]).replace(".0","")
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber","ID", epreop_number)
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_AdvanceSearchButton","ID", "click")
        # sleep(5)
        try_count = 0
        continue_check = False
        while try_count < 6:
            try:
                search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00_ctl04_tdRegisterPatient").click()
                break
            except Exception:
                print('waiting for record')
                try_count += 1
                sleep(1)
                if try_count == 5:
                    continue_check = True
                    break
        if continue_check == True:
            continue

        try:
            Alert(driver).accept()
        except Exception:
            pass
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'Patient Register')))
        wait_until_available('''//div[@id="ctl00_ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_BodyPlaceHolder_RadTabStrip2"]/div/ul/li[2]/a/span/span''',"XPATH", "click")
        rows = driver.find_elements(By.XPATH, '//table[@class="dynamic-table"]/tbody/tr/td/select')
        print("Numrows", len(rows))
        add_provider = True
        for row in rows:
            select = Select(row)
            selected_option = select.first_selected_option
            if num[1] in (selected_option.text).replace(",",""):
                print("Provider already present.")
                add_provider = False
        if add_provider == True:
            wait_until_available("btnAddProvider","ID", "click")
            select = Select(rows[-2])
            select.select_by_value("de8b793f-5750-4b40-8ed4-091a492aa3ee")
            select = Select(rows[-1])
            select.select_by_value(get_provider_name_value(num[1]))
            update_postgre(epreop_number)
        wait_until_available("ctl00_ctl00_ctl00_ContentPlaceHolder_ToolBarPlaceHolder_ToolBarPlaceHolder_btnCancel","ID", "click")
        sleep(1)


def add_medical_review_providers():
    medical_review_nums = getNums("mr")
    for num in medical_review_nums:
        if str(num[0]) == '':
            continue
        driver.switch_to.default_content()
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber","ID", "clear")
        print("data", num)
        epreop_number = str(num[0]).replace(".0","")
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber","ID", epreop_number)
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_AdvanceSearchButton","ID", "click")
        # sleep(5)
        try_count = 0
        continue_check = False
        while try_count < 6:
            try:
                search_by_ID("ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00_ctl04_tdRegisterPatient").click()
                break
            except Exception:
                print('waiting for record')
                try_count += 1
                sleep(1)
                if try_count == 5:
                    continue_check = True
                    break
        if continue_check == True:
            continue

        try:
            Alert(driver).accept()
        except Exception:
            pass
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'Patient Register')))
        wait_until_available('''//div[@id="ctl00_ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_BodyPlaceHolder_RadTabStrip2"]/div/ul/li[2]/a/span/span''',"XPATH", "click")
        rows = driver.find_elements(By.XPATH, '//table[@class="dynamic-table"]/tbody/tr/td/select')
        print("Numrows", len(rows))
        add_provider = True
        for row in rows:
            select = Select(row)
            selected_option = select.first_selected_option
            if num[1] in (selected_option.text).replace(",",""):
                print("Provider already present.")
                add_provider = False
        if add_provider == True:
            wait_until_available("btnAddProvider","ID", "click")
            select = Select(rows[-2])
            select.select_by_value("de8b793f-5750-4b40-8ed4-091a492aa3ee")
            select = Select(rows[-1])
            select.select_by_value(get_provider_name_value(num[1]))
            update_postgre(epreop_number)
        wait_until_available("ctl00_ctl00_ctl00_ContentPlaceHolder_ToolBarPlaceHolder_ToolBarPlaceHolder_btnCancel","ID", "click")
        sleep(1)


def add_provider():

    wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput","ID","clear")
    wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput","ID", "01/01/2019")
    wait_until_available("ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_ToggleAdvanceSearch","ID", "click")
    if len(getNums('cr')) != 0:
        add_clinical_review_providers()
    if len(getNums('mr')) != 0:
        add_medical_review_providers()
    sleep(3)


# MAIN ---------------------------------------------------------------------------------------------

def main():

    if len(getNums('cr')) != 0 or len(getNums('mr')) != 0:
        driver.get("https://gans.epreop.com/OfficeAdmin/clientLogin.aspx")
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName","ID","shshumway")
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password","ID","Gofastgas22")
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_btnSubmit","ID","click")
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
        wait_until_available('''//div[@onclick="javascript:window.parent.showLoader();reDirectTo('/OfficeAdmin/PatientPipeline.aspx')"]''',"XPATH","click")
        add_provider()
        sleep(3)
        cur.close()
        conn.close()
        driver.quit()
    else:
        cur.close()
        conn.close()
        driver.quit()

    # else:
    #     driver.quit()


if __name__ == "__main__":
    main()
