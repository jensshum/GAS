from numpy import insert
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
import os

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://scheduler.intrigma.com/login/entry.bam?ReturnUrl=%2f")

# SEARCH FUNCTIONS ---------------------------------------------------------------------------------------------------

def search_by_ID(id_code):
    search = driver.find_element(By.ID, id_code)
    return search

def search_by_XPATH(Xpath):
    search = driver.find_element(By.XPATH, Xpath)
    return search

# INSERT RECORD INTO MESSAGING TABLE----------------------------------------------------------------------------------
def insert_function(facility_name, clinician_name, phone):
    now = datetime.datetime.now()
    todays_date = (now.strftime('%Y-%m-%d'))
    conn = psycopg2.connect(
        host="cbo-mirror.cbo8fr4pmlfg.us-east-2.rds.amazonaws.com",
        port = "5432",
        user="postgres",
        password= "gr8ergas",
        sslmode="require",
        sslrootcert="SSLCERTIFICATE")

    cur = conn.cursor()
    now = datetime.datetime.now()
    todays_date = (now.strftime('%m/%d/%Y'))
    create_table = '''CREATE TABLE IF NOT EXISTS messaging_table (facility text, clinician text, phone text, date text)'''
    cur.execute(create_table)
    insert_query = '''INSERT INTO messaging_table (facility, clinician, phone, date) VALUES ('%s', '%s', '%s', '%s')''' % (facility_name, clinician_name, phone, todays_date)
    cur.execute(insert_query)
    print("wrote to messaging table")
    conn.commit()

# FIND THE PERSON IN CHARGE FOR THE DAY AT AAC -------------------------------------------------------------------------
def find_acc_person(todays_date):
    print("acc")
    search_by_ID("selectedSections_3_").click()
    search_by_ID("selectedSections_22_").click()
    while driver.find_elements(By.XPATH, '//div[@id="calendarDiv"]/table/tbody/tr') == 0:
        sleep(.5)
        print("slept for table")
    sleep(3)

    search = "day" + str(todays_date)
    print("search", search)

    names = driver.find_elements(By.XPATH, '//table[@id="{}"]/tbody/tr'.format(search))

    # search if Anderson in Day
    Colby = True
    for name in names:
        thing = name.get_attribute('id')
        content = driver.execute_script("return document.getElementById('%s').innerHTML" % thing)
        # print(content)
        facility = "ABRAZO ARROWHEAD CAMPUS"
        if ("Anderson, J.") in str(content):
            if "Chief" in str(content):
                print("chief")
                continue

            else:
                print('Not Chief')
                phone = "(505) 215-0030"
                name = "ANDERSON, JESSICA"
                insert_function(facility, name, phone)
                Colby = False

        else:
            continue

    if Colby == True:
        name = "ALEXANDER, COLBY"
        phone = "(480) 310-0107"
        facility = "ABRAZO ARROWHEAD CAMPUS"
        insert_function(facility, name, phone)

# FIND IRONWOOD BI PERSON -----------------------------------------------------------------------------------------------

def find_bi_person(todays_date):
    print("bi")
    search_by_ID("selectedSections_1_").click()
    search_by_ID("selectedSections_5_").click()

    # Find id with date
    search = "day" + str(todays_date)
    print("search", search)
    sleep(3)

    # Find BoardRunner for the day
    names = driver.find_elements(By.XPATH, '//table[@id="{}"]/tbody/tr'.format(search))
    facility = "BANNER IRONWOOD MEDICAL CENTER"
    i = 1
    Schiche = True
    for name in names:
        # print("i: ", i)
        thing = name.get_attribute('id')
        content = driver.execute_script("return document.getElementById('%s').innerHTML" % thing)
        if "Boardrunner" in str(content):
            print('yes')
            data_title = search_by_XPATH('//table[@id="{}"]/tbody/tr[{}]/td/div'.format(search,i)).get_attribute("data-title")
            name = str(data_title.split("on")[0])
            print(name)
            if "Hitchcock" in name:
                phone = "(435) 660-9736"
                name = "HITCHCOCK, LANDON"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Smith" in name:
                phone = "(480) 329-8468"
                name = "SMITH, SHAWN WYATT"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Broadbent" in name:
                phone = "(801) 830-8299"
                name = "BROADBENT, PAUL"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Bales" in name:
                phone = "(417) 234-5345"
                name = "BALES, AISHA"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Condelee" in name:
                phone = "(616) 403-8775"
                name = "CONDELEE, MAZI"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Veater" in name:
                phone = "(480) 650-1537"
                name = "VEATER, JACOB"
                Schiche = False
                insert_function(facility, name, phone)
                break
            elif "Schiche" in name:
                phone = "(928) 951-2147"
                name = "SCHICHE, HAYLEE JO"
                Schiche = False
                insert_function(facility, name, phone)
                break
        else:
            i += 1
            continue
    if Schiche == True:
        phone = "(928) 951-2147"
        name = "SCHICHE, HAYLEE JO"
        insert_function(facility, name, phone)

# FIND MOUNTAIN VISTA PERSON --------------------------------------------------------------------------------------------
def find_tempe(todays_date):
    print("mv")
    search_by_ID("selectedSections_5_").click()
    search_by_ID("selectedSections_21_").click()

    # Find id with date
    search = "day" + str(todays_date)
    print("search", search)
    sleep(3)

    # Find BoardRunner for the day
    names = driver.find_elements(By.XPATH, '//table[@id="{}"]/tbody/tr'.format(search))
    facility = "TEMPE ST LUKES MEDICAL CENTER"
    i = 1
    Portillos = True
    for name in names:
        # print("i: ", i)
        thing = name.get_attribute('id')
        content = driver.execute_script("return document.getElementById('%s').innerHTML" % thing)
        if "Board" in str(content):
            print('yes')
            def find_name(i):
                print('entered find name function')
                try_count = 1
                while try_count < 10:
                    try:
                        print('entered try block')
                        data_title = search_by_XPATH('//table[@id="{}"]/tbody/tr[{}]/td/div'.format(search,i)).get_attribute("data-title")
                        return data_title
                    except Exception:
                        print("Error. Retrying...")
                        i += 1
                        try_count += 1
                        find_name(i)

            name = str(find_name(i)).split("on")[0]
            print(name)
            if "Weishaar" in name:
                phone = "(602) 762-8528"
                name = "WEISHAAR, SARAH"
                Portillos = False
                insert_function(facility, name, phone)
                break
            elif "Fountain" in name:
                phone = "(480) 414-1295"
                name = "FOUNTAIN, ANGELA"
                Portillos = False
                insert_function(facility, name, phone)
                break
            elif "Portillos" in name:
                phone = "(480) 385-8521"
                name = "JESSICA, PORTILLOS"
                Portillos = False
                insert_function(facility, name, phone)
                break
            elif "Dwiggi" in name:
                phone = "(480) 332-8726"
                name = "DWIGGINS, BRYAN"
                Portillos = False
                insert_function(facility, name, phone)
                break
            elif "Moore" in name:
                phone = "(808) 387-4316"
                name = "MOORE, NICHOLAS"
                Portillos = False
                insert_function(facility, name, phone)
                break
        else:
            i += 1
            continue
    if Portillos == True:
        phone = "(480) 385-8521"
        name = "PORTILLOS, JESSICA"
        insert_function(facility, name, phone)

def find_cath_mountain_vista(todays_date):
    # search_by_ID("selectedSections_21_").click()
    search_by_ID("selectedSections_11_").click()
    search_by_ID("selectedSections_3_").click()
    search_by_ID("selectedSections_22_").click()
    search_by_ID("selectedSections_1_").click()
    # search_by_ID("selectedSections_5_").click()

    search = "day" + str(todays_date)
    sleep(3)

    names = driver.find_element(By.XPATH, '//table[@id="{}"]'.format(search)).text.split("\n")
    for i,name in enumerate(names):
        if 'Cath' in name:
            provider = names[i + 1]
            if 'Stonehocker' in provider:
                provider_name = 'STONEHOCKER, JOSHUA'
                number = '(801) 706-9439'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'Webb' in provider:
                provider_name = 'WEBB, AMANDA'
                number = '(928) 368-3686'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'Call' in provider:
                provider_name = 'CALL, JORDAN'
                number = '(801) 946-4222'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'Thurston' in provider:
                provider_name = 'THRUSTON, AUSTIN'
                number = '(480) 682-8121'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'Hulin' in provider:
                provider_name = 'HULIN, TANNER'
                number = '(574) 303-2241'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'O\'Boyle' in provider or 'Goldammer' in provider:
                provider_name = 'O\'BOYLE, EMILY'
                number = '(308) 631-0944'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)
            elif 'Griffin' in provider:
                provider_name = 'GRIFFIN, GEENA'
                number = '(480) 766-3761'
                insert_function("MOUNTAIN VISTA MEDICAL CENTER CATH", provider_name, number)



# LOGIN TO INTRIGMA ------------------------------------------------------------------------------------------------------
def main():
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "emailAddress"))
        )
    except:
        driver.quit()
    search_by_ID("emailAddress").send_keys("kterhufen@greatergas.com")
    search_by_ID("password").send_keys("Lemons@00")
    search_by_ID("authenticateBtn").click()
    try:
        while len(driver.find_elements(By.XPATH, '//div[@id="headerDiv"]/nav/ul/li[2]/a')) == 0:
            sleep(.5)
            print("slept for thing")
        search_by_XPATH('//div[@id="headerDiv"]/nav/ul/li[2]/a').click()
        while len(driver.find_elements(By.ID, "selectedSections_1_")) == 0:
            sleep(.5)
            print("slept for checklist")
    except Exception as e:
        print(f"an error occurred: {e}")

    now = datetime.datetime.now()
    todays_date = (now.strftime('%Y-%m-%d'))

    find_acc_person(todays_date)
    sleep(1)
    find_bi_person(todays_date)
    sleep(1)
    find_tempe(todays_date)
    sleep(1)
    find_cath_mountain_vista(todays_date)
    insert_function("MOUNTAIN VISTA MEDICAL CENTER", "RYAN, CRAIG", "(480) 734-5333" )
    insert_function("ABRAZO WEST CAMPUS", "RAWLINGS, JAY", "(928) 242-9821" )
    # insert_function("HEADQUARTERS", "PILA, GUILHERME", "(208) 602-9330" )
    # insert_function("HEADQUARTERS", "SHUMWAY, SHELDON", "(801) 556-3431" )

    # driver.quit()
    # find_
if __name__ == "__main__":
    main()
