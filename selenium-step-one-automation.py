
from cgitb import html
from gettext import find
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import timedelta
import datetime
import os

#%% OPEN PROVATION

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# openChrome(PATH, driver)
driver.get("https://gans.epreop.com/OfficeAdmin/clientLogin.aspx")

#%% LOGIN
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName"))
    )
except:
    driver.quit()
search = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_UserName")
search.send_keys("shshumway")
search2 = driver.find_element_by_id("ctl00_ctl00_ContentPlaceHolder_ContentPlaceHolder_LoginForm_ctl05_MALogin_login_Password")
search2.send_keys("Gofastgas22")
search2.send_keys(Keys.RETURN)
sleep(3)
#%% ENTER ANALYTICS
try:
    Xpath = '''//div[@onclick="javascript:window.parent.showLoader();reDirectTo('/OfficeAdmin/reports2.aspx')"]'''
    search = driver.switch_to.frame("RAD_SPLITTER_PANE_EXT_CONTENT_ContentPane")
    element = WebDriverWait(driver,10).until(
        EC.presence_of_element_located((By.XPATH, Xpath))
    )
    search = driver.find_element(By.XPATH, Xpath)
    print('path found')
except Exception as e:
    print(f"Could not locate element: {e}")
    driver.close()
print("Entered Analytics")
search.click()
sleep(2)
#%% ENTER QA SECTION
try:
    search = driver.find_element(By.XPATH, '''//table[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_dlReports"]/tbody/tr[6]/td[2]/div[2]/span''')
    print("Found run element")
except Exception as e:
    print(f"Error loading page. Error: {e}")
    driver.close()
sleep(1)
search.click()
try:
    Xpath = '''//div[@id="divParams"]/div/table/tbody/tr[2]/td[1]/input'''
    element = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.XPATH, Xpath))
    )
    search = driver.find_element(By.XPATH, Xpath)
except Exception as e:
    print(f"Error in the date place: {e}")
#%% ENTER DATES AND DOWNLOAD XML
try:
	element = WebDriverWait(driver, 10).until(
        	EC.presence_of_element_located((By.XPATH, '''//div[@id="divParams"]/div/table/tbody/tr[2]/td[2]/input'''))
    	)
except:
	print("Dates not loaded correctly")
sleep(3)
now = datetime.datetime.now()
todays_date = (now.strftime('%m/%d/%Y'))
yesterday = now - timedelta(days = 1)
yesterdays_date = yesterday.strftime('%m/%d/%Y')
def wait_for_date(search, yesterdays_date):
    try_num = 1
    while try_num < 30:
        try:
            search.send_keys(str(yesterdays_date))
            break
        except Exception:
            print("Error in date. Retrying...")
            try_num += 1
            sleep(1)
wait_for_date(search, yesterdays_date)

search = driver.find_element(By.XPATH, '''//div[@id="divParams"]/div/table/tbody/tr[2]/td[2]/input''')
search.send_keys(str(yesterdays_date))
search = driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_btnRunReport")
search.click()
try:
	element = WebDriverWait(driver, 10).until(
        	EC.presence_of_element_located((By.ID, "ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_ButtonLink")))
except:
	print("The download step took too long to load")
search = driver.find_element(By.ID, "ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_ButtonLink")
search.click()
try:
	element = WebDriverWait(driver, 10).until(
        	EC.presence_of_element_located(By.XPATH, '''//div[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_Menu"]/div[5]/a'''))
except:
	print("The click button for the download didn't load")
search = driver.find_element(By.XPATH, '''//div[@id="ctl00_ctl00_ContentPlaceHolder_BodyPlaceHolder_rptMSRSViewer_ctl05_ctl04_ctl00_Menu"]/div[5]/a''')
search.send_keys(Keys.RETURN)

#%% WAIT FOR THE DOWNLOAD
directory = "C:/Users/Owner/Downloads"
num_files = len(os.listdir(directory))
while num_files == len(os.listdir(directory)):
    sleep(1)
driver.quit()
#%% CONNECT TO STEP ONE WEBPAGE

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://dataportal.greatergas.com/login?next=%2Fprofile")

try:

    element = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.ID, "inputUsername"))
    )
    search = driver.find_element(By.ID, "inputUsername")
    search.send_keys("sheldon")
except Exception as e:
    print(f'There was an error locating the element: {e}')

search = driver.find_element(By.ID, "inputPassword")
search.send_keys("Gofastgas22")
search.send_keys(Keys.RETURN)
#
driver.get("https://dataportal.greatergas.com/automation-step1")

element = WebDriverWait(driver,20).until(
        EC.presence_of_element_located((By.NAME, '''archivo''')
    ))
#%% FIND AND UPLOAD MOST RECENT DOWNLOAD
path = "C:/Users/Owner/Downloads"
os.chdir(path)
files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
newest = files[-1]
print("This is trhe newest file: ", newest)



def watch_file_upload(newest_file):
    # if driver.execute_script('document.getElementById("btnFetch").innerHTML') == 'Processing...':
    #     print("true")
    search = driver.find_element(By.XPATH, "//body/h1")
    print(driver.execute_script("document.body.innerHTML"))
    if (search):
        print("Error page.")
        driver.quit()
        # driver.execute_script("window.history.go(-1)")
        # driver.refresh()
        # upload_file(newest_file)



def upload_file(newest_file):

    search = driver.find_element(By.NAME, "archivo")
    search.send_keys("C:/Users/Owner/Downloads/{}".format(newest_file))
    search = driver.find_element(By.ID, "btnFetch")
    search.click()
    watch_file_upload(newest_file)

try_count = 1
upload_file(newest)
driver.quit()


print('finished search.')
