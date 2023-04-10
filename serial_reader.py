import pandas as pd
import numpy 
import serial
import subprocess
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine, types
from datetime import datetime as dt



#####serial in ubuntu
# cmd = "ls /dev/tty* | grep ACM0"
# result = subprocess.run('ls /dev/tty* | grep ACM0' ,capture_output=True,shell=True)
# com_port = result.stdout.decode('utf-8').strip()

#####windows
com_port = 'COM4'

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
        
        

while True:    
    new_df = pd.DataFrame()
    for x in range(10):        
        data = ser.readline().decode()
        data = data.translate(str.maketrans('','','\r'))
        print(data)
    
        split_line = data.split('*')
        data_line = split_line[0]
        
        split_data = data_line.split(':')
        logger_name = split_data[0]
        sensor_data = split_data[1]
        
        split_sensor_data = sensor_data.split(';')
        sensorA = split_sensor_data[0].split(',')
        sensorB = split_sensor_data[1].split(',')
        sensorC = split_sensor_data[2].split(',')
        sensorD = split_sensor_data[3].split(',')
        
       
        data_to_df = pd.DataFrame(list(zip(sensorA, sensorB, sensorC, sensorD))).transpose()  
        data_to_df = data_to_df.rename(columns={0: "node_id",
                                                1: "accel_id", 
                                                2: "xval", 
                                                3: "yval",
                                                4: "zval"})
        
        new_df = pd.concat([new_df,data_to_df], axis = 0).apply(pd.to_numeric)
        new_df = new_df[["node_id","accel_id","xval","yval","zval"]]
        # name_df = "tilt_{}".format(logger_name.lower())
      
    
    ser.close()
        
    # #average part -- need function?
    node1 = new_df.loc[(new_df['node_id'] == 2707)].mean(axis=0)
    node2 = new_df.loc[(new_df['node_id'] == 2020)].mean(axis=0)
    node3 = new_df.loc[(new_df['node_id'] == 2035)].mean(axis=0)
    node4 = new_df.loc[(new_df['node_id'] ==  555)].mean(axis=0)
        
    df_to_db = pd.DataFrame(list(zip(node1, node2, node3, node4))).transpose()
    df_to_db = df_to_db.rename(columns={0: "node_id",
                                        1: "accel_id", 
                                        2: "xval", 
                                        3: "yval",
                                        4: "zval"})
    
    ts = dt.strptime(split_line[1],'%y%m%d%H%M%S\n').strftime('%Y-%m-%d %H:%M:%S')
    df_to_db["ts"] = ts
    df_to_db = df_to_db[["ts","node_id","accel_id","xval","yval","zval"]].astype(object)
    
    try:
        #######  local db
        connection = mysql.connector.connect(host='localhost',
                                              user='root',
                                              password='senslope',
                                              database='exhibit_db')
        
        #######  MIA-DEMO DB
        # connection = mysql.connector.connect(host='192.168.150.113',
        #                                      user='root',
        #                                      password='dynaslope2023',
        #                                      database='exhibit_db')
        
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)


    #######  local db
    engine = create_engine('mysql://root:senslope@localhost/exhibit_db') # enter your password and database names here
    df_to_db.to_sql('tilt_padta', con=engine, index=False, if_exists='append') # Replace Table_name with your sql table name

    #########   MIA-DEMO DB
    # engine = create_engine('mysql://root:dynaslope2023@192.168.150.113/exhibit_db') 
    # df_to_db.to_sql('tilt_padta', con=engine, index=False, if_exists='append') 


    ser.open()
    new_df = pd.DataFrame(None)







