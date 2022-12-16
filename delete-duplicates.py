from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
from config import username,password
from time import sleep
from datetime import timedelta
import datetime
import time
import sys
import pyautogui as py

# GLOBALS-----------------------------------------------------------------------------------------------------
chrome_options = Options()
py.FAILSAFE = False
# chrome_options.add_argument("--headless")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
URL = "https://gans.epreop.com/OfficeAdmin/clientLogin.aspx"

START_ITEM = 0

print ('starting script')
conn = psycopg2.connect(
    host="cbo-mirror.cbo8fr4pmlfg.us-east-2.rds.amazonaws.com",
    port = "5432",
    user="postgres",
    password= "gr8ergas",
    sslmode="require",
    sslrootcert="SSLCERTIFICATE")

cur = conn.cursor()

# FUNCTIONS -------------------------------------------------------------------------------------------------
def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search

def wait_until_available(search_term, qualifier, item ):
    try_count = 1
    while try_count < 30:
        try:
            if qualifier == "ID":
                if item == "click":
                    search_by_ID(search_term).click()
                elif item == "clear":
                    search_by_ID(search_term).clear()
                elif item == "text":
                    return search_by_ID(search_term).text
                elif item == "RETURN":
                    search_by_ID(search_term).send_keys(Keys.RETURN)
                else:
                    search_by_ID(search_term).send_keys(item)

            elif qualifier == "XPATH":
                if item == "click":
                    search_by_XPATH(search_term).click()
                    # break
                elif item == "clear":
                    search_by_XPATH(search_term).clear()
                elif item == "text":
                    return search_by_XPATH(search_term).text
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
                print(f"Error, {e} Retrying...")
            else:
                print(f"Error, retrying... try count: {try_count}")
            sleep(.5)
            try_count += 1


def get_records_to_delete():
    query2 = '''SELECT epreop_number, procedure_date FROM autoremovedup WHERE reason IS NULL or reason = ''; '''
    cur.execute(query2)
    epreop_numbers = cur.fetchall()
    return epreop_numbers

def get_start_item_index():
    pass

def update_record_in_postgre(number_to_update):
    update_query = '''UPDATE autoremovedup SET reason = 'deleted' WHERE epreop_number = '{}'; '''.format(number_to_update)
    cur.execute(update_query)
    conn.commit()
    print('\"deleted\" written to postgre.')

def begin_search(START_ITEM):

    cases_to_delete = get_records_to_delete()
    if len(str(START_ITEM)) > 5:
        for i in range(len(cases_to_delete)):
            if str(START_ITEM) + '.0' == str(cases_to_delete[i][0]):
                START_ITEM = i
    for i in range(START_ITEM,len(cases_to_delete)):
        date = str(cases_to_delete[i][1])
        epreop_number = str(cases_to_delete[i][0]).replace(".0","")
        # driver.maximize_window()

        driver.switch_to.default_content()
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
        if i > 0:
            wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_ToggleAdvanceSearch','ID', 'click')
        wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput','ID','clear')
        wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcStartDate_dateInput','ID', date)
        wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcEndDate_dateInput','ID', 'clear')
        wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_rdpSimpleSearchProcEndDate_dateInput','ID', date)
        wait_until_available('ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_ToggleAdvanceSearch','ID', 'click')
        wait_until_available('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber"]','XPATH', 'clear')
        wait_until_available('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_txtPreAuthorizationNumber"]','XPATH', epreop_number)
        wait_until_available('//*[@id="ctl00_ctl00_ContentPlaceHolder_ActionBarPlaceHolder_AdvanceSearchButton"]','XPATH', 'click')
        sleep(5)
        if wait_until_available('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00"]/tbody/tr/td/div','XPATH','text') == 'No records to display.':
            update_record_in_postgre(epreop_number)
            continue
        else:
            wait_until_available('//*[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_PatientRecordsGrid_ctl00_ctl04_lnkPatientEnteredInError"]','XPATH','click')
            py.press('enter')
            WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.NAME,'Patient Entered in Error')))
            wait_until_available('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_BodyPlaceHolder_PatientPipelineItemViewModel_View_ctl00_txtReason"]','XPATH','Automated Duplicate Delete')
            wait_until_available('//*[@id="ctl00_ctl00_ctl00_ContentPlaceHolder_ToolBarPlaceHolder_ToolBarPlaceHolder_btnUpdate"]','XPATH','click')
            update_record_in_postgre(epreop_number)

# MAIN ----------------------------------------------------------------------------------------------------

def main():
    start = time.time()
    if len(get_records_to_delete()) == 0:
        pass
    else:
        driver.get(URL)
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName","ID", username)
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password","ID", password)
        wait_until_available("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_btnSubmit","ID","click")
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane')))
        wait_until_available('''//div[@onclick="javascript:window.parent.showLoader();reDirectTo('/OfficeAdmin/PatientPipeline.aspx')"]''','XPATH','click')
        begin_search(START_ITEM)
    end = time.time()
    elapsed_time = end-start
    print("elapsed time in seconds: ", elapsed_time)
    print("Completed Script.")
    driver.quit()
    cur.close()
    conn.close()



if __name__ == "__main__":
    main()
