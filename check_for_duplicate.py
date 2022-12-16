# -*- coding: utf-8 -*-
"""
Created on Tue May  3 10:29:54 2022

@author: Owner
"""

import psycopg2

print ('starting script')
conn = psycopg2.connect(
    host="cbo-mirror.cbo8fr4pmlfg.us-east-2.rds.amazonaws.com",
    port = "5432",
#    database="cbo-mirror",
    user="postgres",
    password= "gr8ergas",
    #password="gr8ergas"
    sslmode="require",
    sslrootcert="SSLCERTIFICATE")
    
print ('connected')
cur = conn.cursor()
print ('cursor created')
cur.execute('SELECT version()')
print ('cursor executed')
db_version = cur.fetchone()
print(db_version)

firstName = ""



       
    
