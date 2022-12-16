import numpy as np
import os
import glob
import re
import hl7

files = "C:\\Users\\Owner\Documents\\GAS\\27 items Abrazo and Steward ADTs"
files2 = "C:\\Users\\Owner\Documents\\GAS\\New Abrazo Items"
folder = os.listdir(files)

i = 0
for file in folder:
    i += 1
    f=open(f'{files}/{file}', 'r')
    msg = f.read()
	# msg = msg.replace('\n', '\r')
	# data = hl7.parse(msg)
    split_msg = msg.split("|")
    new_msg = []
    for item in split_msg:
        if item != "":
            new_msg.append(item)
    f.close()
    new_msg_as_string = ",".join([str(item) for item in new_msg])

    f_out = open(f'{files2}/Abrazo_EditedFile_{i}', 'w')
    f_out.write(new_msg_as_string)
    f_out.close()
