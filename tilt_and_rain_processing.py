# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 15:41:18 2023

@author: aguil
"""
import sys
import pandas as pd
import numpy 
import serial
import subprocess
import mysql.connector
# import MySQLdb
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import re
from mysql.connector import Error
from sqlalchemy import create_engine, types
from datetime import datetime as dt


db = MySQLdb.connect(host = '192.168.150.118',
                     user = 'root',
                     passwd = 'dynaslope2023',
                     db = 'analysis_db')

#####serial in ubuntu
cmd = "ls /dev/tty* | grep ACM0"
result = subprocess.run('ls /dev/tty* | grep ACM0' ,capture_output=True,shell=True)
com_port = result.stdout.decode('utf-8').strip()

cmd2 = "sudo chmod a+rw" + com_port
result = subprocess.run(cmd,capture_output=True,shell=True)
# print (result)

#####windows
# com_port = 'COM7'

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
        
def sensor_parser(data):
    new_df = pd.DataFrame()
    for x in range(10):
        #data = ser.readline().decode()
        print("data inside tilt parser")
        data = data.translate(str.maketrans('','','\r'))
        print(data)
        split_line = data.split('*')
        data_line = split_line[0]
        print("PRINT 1")
        split_data = data_line.split(':')
        logger_name = split_data[0]
        sensor_data = split_data[1]
        print("PRINT 2")
        split_sensor_data = sensor_data.split(';')
        sensorA = split_sensor_data[0].split(',')
        sensorB = split_sensor_data[1].split(',')
        sensorC = split_sensor_data[2].split(',')
        sensorD = split_sensor_data[3].split(',')
        print("POINT 3")
       
        data_to_df = pd.DataFrame(list(zip(sensorA, sensorB, sensorC, sensorD))).transpose()  
        data_to_df = data_to_df.rename(columns={0: "node_id",                            
                                                1: "type_num",
                                                2: "xval", 
                                                3: "yval",
                                                4: "zval"})
        print("POINT 4")
        new_df = pd.concat([new_df,data_to_df], axis = 0).apply(pd.to_numeric)
        print("POINT X")
        print("New df:",new_df)
        new_df = new_df[["node_id","type_num","xval","yval","zval"]]
        print("POINT 5")
        # name_df = "tilt_{}".format(logger_name.lower())
    print("POINT 6")  
    
    #ser.close()
        
    # #average part -- need function?
    node1 = new_df.loc[(new_df['node_id'] == 2707)].mean(axis=0)
    node1['node_id'] = 4
    node2 = new_df.loc[(new_df['node_id'] == 2020)].mean(axis=0)
    node2['node_id'] = 3
    node3 = new_df.loc[(new_df['node_id'] == 2035)].mean(axis=0)
    node3['node_id'] = 2
    node4 = new_df.loc[(new_df['node_id'] ==  555)].mean(axis=0)
    node4['node_id'] = 1
        
    df_to_db = pd.DataFrame(list(zip(node1, node2, node3, node4))).transpose()
    df_to_db = df_to_db.rename(columns={0: "node_id",
                                        1: "type_num",
                                        2: "xval", 
                                        3: "yval",
                                        4: "zval"})
    
    ts = dt.strptime(split_line[1],'%y%m%d%H%M%S\n').strftime('%Y-%m-%d %H:%M:%S')
    df_to_db["ts"] = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    df_to_db["ts_written"] = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    df_to_db["batt"] = 3.3
    df_to_db["is_live"] = 1
    df_to_db = df_to_db[["ts_written","ts","node_id","type_num","xval","yval","zval","batt","is_live"]].astype(object)
    print("df to db:",df_to_db)
    try:
        
        #######  MIA-DEMO DB
        connection = MySQLdb.connect(host='192.168.150.118',
                                              user='root',
                                              password='dynaslope2023',
                                              database='analysis_db')
        
        #if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        print("CLOSE THE CURSOR")
        #engine = create_engine('mysql://root:dynaslope2023@192.168.150.118/analysis_db') # enter your password and database names here
        #print("Point 7")
        #df_to_db.to_sql('tilt_padta', con=engine, index=False, if_exists='append')  # Replace Table_name with your sql table name
        print("Point 8")
        #cursor.close()

    except Error as e:
        print("Error while connecting to MySQL", e)
        pass

    #######  local db
    #engine = create_engine('mysql://root:senslope@localhost/exhibit_db') # enter your password and database names here
    
    engine = create_engine('mysql://root:dynaslope2023@192.168.150.118/analysis_db') # enter your password and database names here
    #print("Point 9",df_to_db)
    df_jose = df_to_db
    #print("Jose",df_jose)
    df_jose.to_sql('tilt_padta', con=engine, index=False, if_exists='append')  # Replace Table_name with your sql table name
    #print("***UMABOT****")
    #########   MIA-DEMO DB
    # engine = create_engine('mysql://root:dynaslope2023@192.168.150.113/exhibit_db') 
    # df_to_db.to_sql('tilt_padta', con=engine, index=False, if_exists='append') 


    #ser.open()
    new_df = pd.DataFrame(None)
    
def rain_parser(data):
    # data=ser.readline().decode()
    data = data.replace("*","&")
    data_split = data.split("&")
    site_name = data_split[0]
    rain = data_split [1]
    ts = dt.now()

    time_stamp = ts.strftime('%y-%m-%d %H:%M:%S')
    create_query = ("INSERT INTO rain_padta"
                    "(ts,rain )" \
                    "VALUES (%s,%s);")
    create_values = (time_stamp,rain)
    cursor = db.cursor()
    cursor.execute(create_query, create_values)
    db.commit()
    cursor.close()


while True:        
    data=ser.readline().decode()
    print(data)
    if re.search(',',data):
       try:
        sensor_parser(data)
       except:
        print("Skipping Duplicate Entry...")
    elif re.search('&',data):
        rain_parser(data)
        
        
# try:
#     while True:          
#         data = ser.readline().decode()
#         data_split = data.split(",")
#         ts = data_split[0]
#         rain = data_split [1]
#         rain = rain.strip() #removes \r\n
#         #print(rain)
#         lst = [ts, rain]
#         df = pd.DataFrame([lst])
#         df.columns =['ts','rain']
#         print(df)
        
#         engine = create_engine('mysql://root:senslope@localhost/senslopedb') # enter your password and database names here
#         df.to_sql('rain_padra', con=engine, index=False, if_exists='append') # Replace Table_name with your sql table name
# except KeyboardInterrupt:

#     ser.close()

# finally:

#     ser.close()






