import PyPDF2
import datetime
from datetime import timedelta
import os

NOW = datetime.datetime.now()
TODAY = NOW.strftime('%m/%d/%Y')
TOMORROW = NOW + timedelta(days = 1)
YESTERDAY = NOW - timedelta(days = 1)
YESTERDAYS_DATE = YESTERDAY.strftime('%m/%d/%Y')
TOMORROW_DATE = TOMORROW.strftime('%m/%d/%Y')
today = NOW.strftime('%m %d')
download_date_folder = NOW.strftime('%m %d') + " DOWNLOAD DOS " + YESTERDAY.strftime("%m %d") + " CASES"
date_to_use = YESTERDAYS_DATE

pdf_file_obj = open('C:/Users/Owner/Downloads/FOREST_CANYON_CBO_DOWNLOAD_{}.pdf'.format(date_to_use.replace("/","-")),'rb')

pdfReader = PyPDF2.PdfFileReader(pdf_file_obj) 

num_pages = pdfReader.numPages
patient_array = []
for i in range(num_pages):
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = pdfReader.getPage(i) 
    name = pageObj.extractText().split('\n')[2].split(':')[1]
    name = name.split(" ")[0] + " " + name.split(" ")[1]
    # print(name)
    patient_array.append(name)

    pdfWriter.add_page(pdfReader.pages[i])

    patient_folder = False
    for patient_folder_name in os.listdir("C:/Users/Owner/Greater Anesthesia Dropbox/Sheldon Shumway/CBO folder/" + download_date_folder + "/FCESC"):
        if name.upper() in patient_folder_name:
            with open("C:/Users/Owner/Greater Anesthesia Dropbox/Sheldon Shumway/CBO folder/" + download_date_folder + "/FCESC/" + patient_folder_name + "/{}_{}.pdf".format(name.upper(),date_to_use.replace("/","-")), "wb") as f:
                pdfWriter.write(f)
            patient_folder = True
            break
    
    if patient_folder == False:
        os.mkdir("C:/Users/Owner/Greater Anesthesia Dropbox/Sheldon Shumway/CBO folder/" + download_date_folder + "/FCESC/" + name.upper())
        with open("C:/Users/Owner/Greater Anesthesia Dropbox/Sheldon Shumway/CBO folder/" + download_date_folder + "/FCESC/" + name.upper() + "/{}_{}.pdf".format(name.upper(),date_to_use.replace("/","-")), "wb") as f:
            pdfWriter.write(f)
        continue

pdf_file_obj.close()

with open("C:/Users/Owner/Documents/GAS/forest_canyon_patients/forest_canyon_patient_names_{}.txt".format(date_to_use.replace("/","_")),'x') as f:
    for patient in patient_array:
        f.write(patient + "\n")

