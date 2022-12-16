# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:29:39 2022

@author: Owner
"""

import csv
import os

folder = "C:\\Users\\Owner\\Documents\\GAS\\globe_az-20220330"
folder2 = "CSV_FILES"
files = os.listdir(folder)
# os.mkdir("CSV_FILES")
i = 0
import csv
for file in files:
    if file.endswith(".psv"):
        with open(f'{folder}/{file}', "r") as file_pipe:
            reader_pipe = csv.reader(file_pipe, delimiter='|')
            with open(f'{folder2}/{file}0.csv', 'w') as file_comma:
                writer_comma = csv.writer(file_comma, delimiter=',')
                for row in reader_pipe:
                    writer_comma.writerow(row)
        
      
        
        
    

    
    