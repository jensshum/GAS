import jinja2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
from datetime import date, timedelta
import datetime
import pandas as pd
import os
from selenium.webdriver import ActionChains
import pyautogui as py
# GLOBALS---------------------------------------------------------------------------------

now = datetime.datetime.now()
TODAYS_DATE = (now.strftime('%#m/%#d/%Y'))
yesterday = now - timedelta(days = 1)
YESTERDAYS_DATE = yesterday.strftime('%#m/%#d/%Y')
tomorrow = now + timedelta(days = 1)
TOMORROWS_DATE = tomorrow.strftime('%Y-%m-%d')
date_to_use = now.strftime('%m_%d_%Y')
date_folder = now.strftime("%m %d") + " DOWNLOAD DOS " + yesterday.strftime("%m %d") + " CASES"
PATH = "C:\Program Files (x86)\msedgedriver.exe"
driver = webdriver.Edge(PATH)
action = ActionChains(driver)

# driver.set_window_size(1024, 600)


# FUNCTIONS --------------------------------------------------------------------------------

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search


def wait_until_available(search_term, qualifier, item):
    try_count = 1
    while try_count <= 8:
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

def go_back_to_scheduler():
    driver.switch_to.default_content()
    driver.switch_to.frame("fraDefault")
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'panMenu_Frame')))
    search_by_XPATH('//*[@id="tabMyActivities_Center"]/table/tbody/tr[1]').click()
    search_by_XPATH('//*[@id="tabMyActivities_Center"]/table/tbody/tr[1]').click()

def click_print(patient_name,iteration):
    driver.execute_script(
    '''var targLink = document.querySelectorAll(".ToolbarMediumButtonMouseOut")[4];
    var clickEvent  = document.createEvent('MouseEvents');
    clickEvent.initEvent('click', true, true);
    targLink.dispatchEvent(clickEvent);''')
    if iteration == 1:
        sleep(10)
        py.press('tab')
        py.press('tab')
        py.press('enter')
        for i in range(10):
            py.press('up')
        py.press('enter')
        sleep(3)
    else:
        sleep(10)
        py.press('tab')
        py.press('tab')
    for i in range(5):
        py.press('tab')
    py.press('enter')
    sleep(3)
    py.press('backspace')
    os.mkdir("C:/Users/Owner\/Greater Anesthesia Dropbox/Sheldon Shumway/CBO folder/" + date_folder + "/CAGLI/" + patient_name.upper())
    py.write("C:\\Users\\Owner\\Greater Anesthesia Dropbox\\Sheldon Shumway\\CBO folder\\" + date_folder + "\\CAGLI\\" + patient_name.upper() + "\\" + str(patient_name).upper() + " SBILL+ANES_NOTE " + str(YESTERDAYS_DATE).replace("/",'-') + ".pdf")
    py.press('enter')
    sleep(7)
    go_back_to_scheduler()
    

def iterate_through_rows(procedure,iteration):
    print(procedure)
    driver.switch_to.default_content()
    driver.switch_to.frame("fraDefault")
    print("ITERATION,", iteration)
    frames = driver.find_elements(By.XPATH,'//*[@id="MainPanes"]/div')
    # print(frames[1].get_attribute("id"))
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, frames[iteration].get_attribute("id").replace("_Div","_Frame"))))
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"fraTree_Frame")))
    rows = driver.find_elements(By.XPATH,'//*[@id="ctl00_treChart_RadTreeView"]/ul/li/div/span[3]')
    print(len(rows))
    sleep(2)
    for i,row in enumerate(rows):
        row_text = driver.execute_script('''return document.querySelectorAll("#ctl00_treChart_RadTreeView > ul > li")[{}].innerText;'''.format(i))
        print(row_text)
        # print(YESTERDAYS_DATE)
        if procedure and YESTERDAYS_DATE in row_text:
            try:
                action.double_click(row).perform()
            except Exception:
                driver.execute_script('''var targLink = document.querySelectorAll(".rtIn")[{}];
                var clickEvent  = document.createEvent('MouseEvents');
                clickEvent.initEvent('dblclick', true, true);
                targLink.dispatchEvent(clickEvent);'''.format(i))
                print('clicked') 
            break
    # kill
    driver.switch_to.default_content()
    driver.switch_to.frame("fraDefault")
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, frames[iteration].get_attribute("id").replace("_Div","_Frame"))))
    # //*[@id="tabChart_DIVtabPagebd0dd149-6d94-44af-ac3d-21add4a9f026"]
    sub_frame = driver.find_element(By.XPATH,"//tr[@id='tabChart_Containers']/td/table/tbody/tr/td/div[2]").get_attribute("id").replace("tabChart_DIVtabPage",'fra') + "_Frame"
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, sub_frame)))
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'fraDocument_Frame')))
    driver.execute_script(
    '''var targLink = document.querySelectorAll(".ToolbarMediumButtonMouseOut")[0];
    var clickEvent  = document.createEvent('MouseEvents');
    clickEvent.initEvent('click', true, true);
    targLink.dispatchEvent(clickEvent);''')
    print(row_text)
    driver.switch_to.default_content()
    driver.switch_to.frame("fraDefault")
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, frames[iteration].get_attribute("id").replace("_Div","_Frame"))))
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID, sub_frame)))
    driver.execute_script(
    '''var targLink = document.querySelectorAll(".checkboxSelection")[1];
    var clickEvent  = document.createEvent('MouseEvents');
    clickEvent.initEvent('click', true, true);
    targLink.dispatchEvent(clickEvent);''')
    row_names = driver.find_elements(By.XPATH,'//*[@id="tblList_Table"]/tbody/tr')
    for i,row in enumerate(row_names):
        if row.text == 'Anesthesia Note' or 'GI Superbill' in row.text:
            print("MATCHHHHHH:",i)
            driver.execute_script(
            '''var targLink = document.querySelectorAll("#tblList_Table > tbody > tr > td > input")[{}];
            var clickEvent  = document.createEvent('MouseEvents');
            clickEvent.initEvent('click', true, true);
            targLink.dispatchEvent(clickEvent);'''.format(i))

def close_popup():
    try_count = 0 
    driver.switch_to.default_content()
    driver.switch_to.frame("fraDefault")
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"Popup_Frame")))
    while try_count < 5:
        try:
            search_by_XPATH('//*[@id="btnClose_Table"]').click()
            break
        except Exception:
            try_count += 1
            sleep(1)

def procedure_complete(procedure,name,j):
    print('PROCEDUREEEEE',procedure)
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"DialogBox_Frame")))
    wait_until_available('//*[@id="tbrEdit"]/table/tbody/tr/td[2]/table/tbody/tr/td[15]','XPATH','click')
    close_popup()
    iterate_through_rows(procedure,j)
    # go_back_to_scheduler()
    click_print(name,j)

def no_show():
    go_back_to_scheduler()

def in_progress():
    pass

# MAIN ------------------------------------------------------------------------------------
def main():
    driver.get("https://az-10068-m.ggastrocloud.com/gGastro/")
    # driver.maximize_window()

    driver.switch_to.frame("fraDefault")
    search_by_ID("txtUserName_TextBox").send_keys("kterhufen")
    search_by_ID("txtPassword_TextBox").send_keys("Yellow@34")
    search_by_ID("btnLogin_Table").click()
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"panTask_Frame")))
    # break
    # search_by_ID('btnsnpAppointmentPrevious').click()
    sleep(10)
    rows = ''
    while len(rows) == 0:
        try:
            rows = driver.find_elements(By.XPATH,'//*[@id="tblAppointmentsnpAppointment_Table"]/tbody/tr')
        except Exception:
            pass
    j = 1
    for i,row in enumerate(rows[1:],1):
        driver.switch_to.default_content()
        driver.switch_to.frame('fraDefault')
        WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"panTask_Frame")))
        text = driver.execute_script('''return document.querySelectorAll("#tblAppointmentsnpAppointment_Table > tbody > tr")[{}].innerText;'''.format(i))
        procedure = text.split('\t')[1]
        name = text.split('\t')[3]
        status = text.split('\t')[4].replace("\n",'')

        driver.execute_script('''var targLink = document.querySelectorAll("#tblAppointmentsnpAppointment_Table > tbody > tr")[{}];
                                var clickEvent  = document.createEvent('MouseEvents');
                                clickEvent.initEvent('click', true, true);
                                targLink.dispatchEvent(clickEvent);'''.format(i))
        
        print(status)

        if status == "Post-Op call completed" or status == "Procedure Completed" or status == "Post-Op Call Attempted":
            procedure_complete(procedure,name,j)
            j += 1
        elif status == 'No Show':
            continue
        elif status == "In Progress":
            in_progress()
        
        continue
    driver.quit()



if __name__ == "__main__":
    main()