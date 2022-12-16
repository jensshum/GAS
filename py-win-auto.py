from pywinauto.application import Application as ap
import pyautogui as py
from datetime import timedelta
import datetime
from time import sleep
import os

#GLOBAL--------------------------------------------------------------------------------------------

NOW = datetime.datetime.now()
TODAY = NOW.strftime('%m/%d/%Y')
TOMORROW = NOW + timedelta(days = 1)
YESTERDAY = NOW - timedelta(days = 1)
YESTERDAYS_DATE = YESTERDAY.strftime('%m/&d/%Y')
folder_name = NOW.strftime('%m %d') + " DOWNLOAD DOS " + YESTERDAY.strftime('%m %d') + " CASES"
# folder_name = "08 02" + " DOWNLOAD DOS " + "08 01" + " CASES"
TOMORROW_DATE = TOMORROW.strftime('%m/%d/%Y')
today = NOW.strftime('%m %d')

app_title = "Connect Back Office 22.3.5 [Shumway, Sheldion] [globe-az]"

# FUNCTION ---------------------------------------------------------------------------------------

def abrazo_cases():
    
    base_folder = "C:/Users/Owner/Greater Anesthesia Dropbox/sheldon shumway/CBO folder/"
    for facility_folder in os.listdir(base_folder + folder_name):
        facility_path = base_folder + folder_name + "/" + facility_folder
        print("Folder: ", facility_path)

        if len(os.listdir(facility_path)) == 0:
            print('Skipped')
            continue
        else:
            file_count = 0
            skip = True
            for file in os.listdir(facility_path):
                if file.startswith(facility_folder):
                    skip = True
                elif file.startswith('MV'):
                    skip = True
                else:
                    skip = False
                    file_count += 1
            if skip == True:
                continue
            
       
        dos = folder_name.split('DOS')[1].replace("CASES","")
        facility_code = str(facility_folder)
        # total_cases = str(len(os.listdir(base_folder + folder_name + "/" + facility_folder)) - 2)
        gas_to_code = False
        
        batch_description = dos + " " + facility_code + " " + str(file_count)
        py.write(batch_description)
        py.press('tab')
        py.press('tab')
        py.press('tab')
        print(facility_code)
        if facility_code == 'AAC':
            for i in range(20):
                py.press('up')
            py.press('down')
        elif facility_code == 'AU':
            for i in range(20):
                py.press('up')
            for i in range(5):
                py.press('down')
        elif facility_code == 'AWC':
            for i in range(20):
                py.press('up')
            for i in range(4):
                py.press('down')
        elif facility_code == 'BGMC':
            for i in range(20):
                py.press('up')
            for i in range(7):
                py.press('down')
        elif facility_code == 'BIMC':
            for i in range(20):
                py.press('up')
            for i in range(8):
                py.press('down')
        elif facility_code == 'CAGLI':
            for i in range(20):
                py.press('up')
            for i in range(11):
                py.press('down')
        elif facility_code == 'FCESC':
            for i in range(20):
                py.press('up')
            for i in range(13):
                py.press('down')
        elif facility_code == 'FH':
            for i in range(20):
                py.press('up')
            for i in range(12):
                py.press('down')
        elif facility_code == 'MVMC':
            for i in range(20):
                py.press('up')
            for i in range(15):
                py.press('down')
        elif facility_code == 'TSL':
            for i in range(20):
                py.press('up')
            for i in range(19):
                py.press('down')
        py.press('tab')
        py.write(dos.replace(" ","") + "2022")

        for i in range(3): 
            py.press('tab')
        py.press('enter')
        sleep(3)
        py.click(1889, 47)
        sleep(3)

        
        for patient_folder in os.listdir(base_folder + folder_name + "/" + facility_folder):
            if patient_folder.startswith(facility_folder):
                continue
            elif facility_folder == "MVMC" and patient_folder.startswith("MV"):
                continue
            
            else:
                for file in os.listdir(base_folder + folder_name + '/' + facility_folder + '/' + patient_folder):
                    if file.endswith('pdf'):
                        py.write("\"" + base_folder + folder_name + '/' + facility_folder + '/' + patient_folder + '/' + file + "\" ")
                        sleep(.5)
                    else:
                        continue
                py.press('enter')
                # wait for upload to finish
                sleep(15)
                #click on create new set
                if patient_folder != os.listdir(base_folder + folder_name + "/" + facility_folder)[-1]:
                    py.click(87, 123)
                    sleep(3)
                    py.click(1889, 47)
                    sleep(3)
        # wait for final upload
        sleep(10)  
        py.click(1887, 8)
        sleep(3)
        # click create new batch
        py.click(1858, 211)
        sleep(4)
        py.write('')

# MAIN --------------------------------------------------------------------------------------------

def main():
    app = ap(backend='uia').connect(title=app_title,timeout=10)
    sleep(1
    )
    dlg = app["ConnectBackOffice22.3.3[Shumway,Sheldion][globe-az]"]
    # dlg.Maximize.click_input()
    # click on 'manage'
    py.click(120, 40)
    # tab until image batches
    for i in range(9):
        py.press('tab')
    py.press('enter')
    sleep(3)
    # click enter for error messages
    for i in range(6):
        py.press('enter')
    # click create new batch
    py.click(1858, 209)

    py.press('enter')
    sleep(3)

    abrazo_cases()

    # dlg.Maximize.click_input()
    
if __name__ == "__main__":
    main()