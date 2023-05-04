# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:41:18 2023

@author: aguilar
"""

import pandas as pd
import numpy 
import serial
import subprocess
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, types
from datetime import datetime as dt



#####serial in ubuntu
cmd = "ls /dev/tty* | grep ACM0"
result = subprocess.run('ls /dev/tty* | grep ACM0' ,capture_output=True,shell=True)
com_port = result.stdout.decode('utf-8').strip()

cmd2 = "sudo chmod a+rw " + com_port
result = subprocess.run(cmd2 ,capture_output=True,shell=True)

#####windows
# com_port = 'COM3'

#df = pd.DataFrame(columns=['ts' , 'rain'])
#print(df)


try:
        ser = serial.Serial(
                port = (com_port),\
                baudrate = 9600,\
                parity = serial.PARITY_NONE,\
                stopbits = serial.STOPBITS_ONE,\
                bytesize = serial.EIGHTBITS,\
                timeout = None)
        print ('connected to port {}'.format(com_port))
        
except serial.SerialException:
        print ("ERROR: Could Not Open COM %r!" % (com_port))
        
        
try:
    while True:          
        data = ser.readline().decode()
        data_split = data.split(",")
        ts = data_split[0]
        rain = data_split [1]
        rain = rain.strip() #removes \r\n
        #print(rain)
        lst = [ts, rain]
        df = pd.DataFrame([lst])
        df.columns =['ts','rain']
        print(df)
        
        engine = create_engine('mysql://root:senslope@localhost/analysis_db') # enter your password and database names here
        df.to_sql('rain_padta', con=engine, index=False, if_exists='append') # Replace Table_name with your sql table name
except KeyboardInterrupt:

    ser.close()

finally:

    ser.close()







