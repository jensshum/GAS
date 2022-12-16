import hl7
import os
import psycopg2
from pandas.core.common import flatten
from datetime import date


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
    
# print ('connected')
cur = conn.cursor()
# print ('cursor created')
cur.execute('SELECT version()')
# print ('cursor executed')
db_version = cur.fetchone()
# print(db_version)

folder = 'C:\\Users\\Owner\\Documents\\GAS\\Steward Files'
files = os.listdir(folder)
i = 0
patient_id_number=""
message_number=""
admission_date=""
discharge_date=""
for file1 in files:
    with open(f'{folder}/{file1}', 'r') as file:
        # print("This is the file: ", f"{file1}")
        msg = file.read()
        # if ('PR1') in msg:
        # try:
        msg = msg.replace('\n', '\r')
        data = hl7.parse(msg)
        patient_id_number = data['PID'][0][3][0][0][0]
        message_number = data['MSH'][0][10][0]
        facility = data['MSH'][0][4][0]
        if len(data['PID'][0][5][0]) > 2:    
            middle_name = data['PID'][0][5][0][2][0]
        else: 
            middle_name = 'None'
        last_name = data['PID'][0][5][0][0][0]
        first_name = data['PID'][0][5][0][1][0]
        date_of_birth = data['PID'][0][7][0]
        gender = data['PID'][0][8][0]
        social_security_number = data['PID'][0][19][0]
        line_1 = data['PID'][0][11][0][0][0]
        line_2 = data['PID'][0][11][0][1][0]
        zipcode = data['PID'][0][11][0][4][0]
        city = data['PID'][0][11][0][2][0]
        if len(data['PID']) > 1:
            daytime_phone = data['PID'][0][13][0][0][0]
        else:
            daytime_phone = "None"
        state = data['PID'][0][11][0][3][0]
        marital_status = data['PID'][0][16][0]
        room = data['PV1'][0][3][0]
        if len(data['PID'][0]) > 25:
            admission_date = data['PV1'][0][44][0]
            discharge_date = data['PV1'][0][45][0]
        if 'GT1' in msg:
            gua_gender = data['GT1'][0][9][0]
            gua_last_name = data['GT1'][0][3][0][0][0]
            gua_first_name = data['GT1'][0][3][0][1][0]
            if len(data['GT1'][0][3][0]) > 2:
                gua_middle_name = data['GT1'][0][3][0][2][0]
            else:
                gua_middle_name = 'None'
            gua_line_1 = data['GT1'][0][5][0][0][0]
            gua_line_2 = data['GT1'][0][5][0][1][0]
            gua_city = data['GT1'][0][5][0][2][0]
            gua_state = data['GT1'][0][5][0][3][0]
            gua_zipcode = data['GT1'][0][5][0][4][0]
            gua_daytime_phone = list(flatten(data['GT1'][0][6][0]))
        else:
            gua_gender = ""
            gua_last_name = ""
            gua_first_name = ""
            gua_middle_name = '' 
            gua_middle_name = ''
            gua_line_1 = ''
            gua_line_2 = ''
            gua_city = ''
            gua_state = ''
            gua_zipcode = ''
            gua_daytime_phone = ''
        if 'IN1' in msg:
            member_number = data['IN1'][0][8][0]
            plan = data['IN1'][0][2][0]
            if len(data['IN1'](0)) < 12:
                patient_relationship_to_subscriber = data['IN1'][0][17][0]
                preauthorization_number = data['IN1'][0][14][0]
            else:
                patient_relationship_to_subscriber = ""
                preauthorization_number = ''
        else: 
            member_number = ""
            plan= "No insurance"
            patient_relationship_to_subscriber = ''
            preauthorization_number = ''
            
        facility_case_number = data['PV1'][0][1][0]
        if len(data['PV1'][0][9][0]) > 3:
            rendering_physician = data['PV1'][0][9][0][1][0] + ", " + data['PV1'][0][9][0][2][0]
        else:
            rendering_physician = ''
        physical_status = data['PV1'][0][4][0]
        start_time = ""
        end_time =""
        emergency = ""
        if 'PR1' in msg:
            Procedure_Code = data['PR1'][0][3][0]
            Procedure_Description = data['PR1'][0][4][0]
            Procedure_Type = data['PR1'][0][6][0]
            Procedure_Time = data['PR1'][0][5][0]
            if len(data['PR1'][0]) > 7:
                Anesthesiologist = data['PR1'][0][8][0]
                AnesthesiaCode = data['PR1'][0][9][0]
                Anesthesia_Time = data['PR1'][0][10][0]
                Surgeon = list(flatten(data['PR1'][0][11][0]))
                Procedure_Practitioner = data['PR1'][0][12][0]
            else:
                Anesthesiologist = "N/A"
                AnesthesiaCode = "N/A"
                Anesthesia_Time = "N/A"
                Surgeon = "N/A"
                Procedure_Practitioner = "N/A"
            if len(data['PR1']) > 1:
                Procedure_Code_2 = data['PR1'][1][3][0]
                Procedure_Description_2 = data['PR1'][1][4][0]
                Procedure_Type_2 = data['PR1'][1][6][0]
                Procedure_Time_2 = data['PR1'][1][5][0]
                if len(data['PR1'][1]) > 7:
                    Anesthesiologist_2 = data['PR1'][1][8][0]
                    AnesthesiaCode_2 = data['PR1'][1][9][0]
                    Anesthesia_Time_2 = data['PR1'][1][10][0]
                    Surgeon_2 = list(flatten(data['PR1'][1][11][0]))
                    Procedure_Practitioner_2 = data['PR1'][1][12][0]
            else:
                Procedure_Code_2 = ""
                Procedure_Description_2 = ""
                Procedure_Type_2 = ""
                Procedure_Time_2 = ""
                Anesthesiologist_2 = ""
                AnesthesiaCode_2 = ""
                Anesthesia_Time_2 = ""
                Surgeon_2 = ""
                Procedure_Practitioner_2 = ""
        else:
            Procedure_Code = ""
            Procedure_Description = ""
            Procedure_Type = ""
            Procedure_Time=""
            Anesthesiologist = ""
            AnesthesiaCode = ""
            Anesthesia_Time = ""
            Surgeon = ""
            Procedure_Practitioner = ""
            Anesthesiologist = ""
            AnesthesiaCode = ""
            Anesthesia_Time = ""
            Surgeon = ""
            Procedure_Practitioner = ""
            Procedure_Code_2 = ""
            Procedure_Description_2 = ""
            Procedure_Type_2 = ""
            Procedure_Time_2 =""
            Anesthesiologist_2 = ""
            AnesthesiaCode_2 = ""
            Anesthesia_Time_2 = ""
            Surgeon_2 = ""
            Procedure_Practitioner_2 = ""
            Anesthesiologist_2 = ""
            AnesthesiaCode_2 = ""
            Anesthesia_Time_2 = ""
            Surgeon_2 = ""
            Procedure_Practitioner_2 = ""
            
            
            
            
        # except Exception:
        #     print(Exception)
            
        create_script = ''' CREATE TABLE IF NOT EXISTS Steward_Adts (
            Patient_ID_Number varchar(20),
            Message_ID_Number varchar(20),
            ADT_record_number varchar(20),
            facility varchar(10) NOT NULL,
            middle_name varchar(50),
            first_name varchar(50),
            last_name varchar(50) NOT NULL,
            date_of_birth varchar(10) NOT NULL,
            gender varchar(3) NOT NULL,
            social_security_number varchar(15) NOT NULL,
            line_1 varchar(50) NOT NULL,
            line_2 varchar(50) NOT NULL,
            zipcode varchar(10),
            city varchar(100),
            state varchar(50),
            marital_status varchar(10),
            room varchar(50),
            admission_date varchar(30),
            discharge_date varchar(30),
            guarantor_gender varchar(1),
            guarantor_last_name varchar(50),
            guarantor_first_name varchar(50),
            guarantor_middle_name varchar(50),
            guarantor_line_1 varchar(100),
            guarantor_line_2 varchar(100),
            guarantor_city varchar(100),
            guarantor_state varchar(50),
            guarantor_zipcode varchar(20),
            guarantor_daytime_phone varchar(50),
            plan varchar(20),
            patient_relationship_to_subscriber varchar(10),
            facility_case_number varchar(20),
            member_number varchar(30),
            rendering_physician varchar(100),
            physical_status varchar(20),
            start_time varchar(20),
            end_time varchar(20),
            preauthorization_number varchar(100),
            emergency varchar(10),
            procedure_code varchar(10),
            procedure_description varchar(200),
            procedure_type varchar(20),
            procedure_time varchar(10),
            anesthesiologist varchar(50),
            anesthesia_code varchar(30),
            anesthesia_time varchar(20),
            surgeon varchar(50),
            procedure_practitioner varchar(60),
            Procedure_Code_2 varchar(10),
            Procedure_Description_2 varchar(200),
            Procedure_Type_2 varchar(20),
            Procedure_Time_2 varchar(10),
            Anesthesiologist_2 varchar(50),
            AnesthesiaCode_2 varchar(30),
            Anesthesia_Time_2 varchar(20),
            Surgeon_2 varchar(50),
            Procedure_Practitioner_2 varchar(60)
            )'''
    
        cur.execute(create_script)
        
        
        today = date.today()
        serial_number = f"{today}_ADT_{i}"
        i += 1
        insert_script = ('INSERT INTO Steward_Adts (Patient_ID_Number, Message_ID_Number, ADT_record_number, facility, middle_name, first_name,last_name,date_of_birth,gender,social_security_number,line_1,line_2,zipcode,city,state,marital_status, room,admission_date,discharge_date,guarantor_gender,guarantor_last_name,guarantor_first_name, guarantor_middle_name,guarantor_line_1,guarantor_line_2,guarantor_city,guarantor_state,guarantor_zipcode,guarantor_daytime_phone, plan,patient_relationship_to_subscriber,facility_case_number,member_number,rendering_physician,physical_status,start_time,end_time,preauthorization_number,emergency,procedure_code, procedure_description, procedure_type, procedure_time, anesthesiologist, anesthesia_code, anesthesia_time,surgeon, procedure_practitioner,Procedure_Code_2,Procedure_Description_2,Procedure_Type_2,Procedure_Time_2,Anesthesiologist_2,AnesthesiaCode_2,Anesthesia_Time_2,Surgeon_2,Procedure_Practitioner_2 )' 
                          'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
        
        
        
        insert_values = [patient_id_number, message_number, serial_number,facility,middle_name,first_name,last_name,date_of_birth,gender,social_security_number,line_1,line_2,zipcode,city,state,marital_status, room,admission_date,discharge_date,gua_gender,gua_last_name,gua_first_name, gua_middle_name,gua_line_1,gua_line_2,gua_city,gua_state,gua_zipcode,gua_daytime_phone, plan,patient_relationship_to_subscriber,facility_case_number,member_number,rendering_physician,physical_status,start_time,end_time,preauthorization_number,emergency,Procedure_Code, Procedure_Description, Procedure_Type, Procedure_Time, Anesthesiologist, AnesthesiaCode, Anesthesia_Time,Surgeon, Procedure_Practitioner, Procedure_Code_2, Procedure_Description_2,Procedure_Type_2, Procedure_Time_2,Anesthesiologist_2,AnesthesiaCode_2,Anesthesia_Time_2,Surgeon_2, Procedure_Practitioner_2]
        cur.execute(insert_script, insert_values)
        
    
    
delete_duplicates_query = (''' 
DELETE FROM Steward_Adts
WHERE adt_record_number in (
SELECT adt_record_number 
FROM (
SELECT adt_record_number,
ROW_NUMBER() OVER (PARTITION BY first_name, last_name, middle_name) AS rownum
FROM Steward_Adts
) AS sub
WHERE rownum > 1);
''')

cur.execute(delete_duplicates_query)
conn.commit()

cur.close()
conn.close()









