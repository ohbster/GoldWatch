import json
import sys
import os
import logging
import pymysql
import boto3
from botocore.exceptions import ClientError
from get_parameter import *
from get_connection import * 


connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    print("Creating Table")
    cursor = connection.cursor()
    
    #For development. Crop existing tables if needed
    
    #cursor.execute('''DROP TABLE IF EXISTS GoldPrice; ''')
    #cursor.execute('''DROP TABLE IF EXISTS Historical_Data; ''')
    #cursor.execute('''DROP TABLE IF EXISTS Alerts_Low;''')
    cursor.execute('''DROP TABLE IF EXISTS Alerts_High;''')
    #connection.commit()
    
    #Table for daily price info
    cursor.execute('''CREATE TABLE IF NOT EXISTS GoldPrice(
    Daystamp DATE PRIMARY KEY NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Current REAL NOT NULL
    );
    ''')
    
    #Table for historical price info. (Prices from api.metal.live)
    cursor.execute('''CREATE TABLE IF NOT EXISTS Historical_Data(
    Price REAL NOT NULL,
    Time_Stamp BIGINT UNSIGNED PRIMARY KEY NOT NULL
    ); ''')
        
    #Alerts if price goes below a target
    #!!! Need to have a composite key with time_created and email
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_Low(
    Email VARCHAR(320) PRIMARY KEY NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1,
    Time_Created BIGINT UNSIGNED NOT NULL,
    Last_Checked BIGINT UNSIGNED NOT NULL
    );
    ''')
    
    #Alerts if price goes above a certain target
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_High(
    Email VARCHAR(320) PRIMARY KEY NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1,
    Time_Created BIGINT UNSIGNED NOT NULL,
    Last_Checked BIGINT UNSIGNED NOT NULL
    );    
    ''')
    #cursor.execute('''INSERT INTO GoldPrice (Day, High, Low, Current)
    #VALUES (0000-00-00, 0.00, 0.00, 0.00);
    #''')
    
    #cursor.execute('''INSERT INTO GoldPrice (Daystamp, High, Low, Current)
    #VALUES ('2022-10-01', 1.00, 2.00, 3.00);
    #''')
    
    #cursor.execute('''SELECT * FROM GoldPrice''')
    
    
    #multiplic the UNIX_TIMESTAMP by 1000 since price data is in milliseconds
    cursor.execute('''INSERT INTO Alerts_High (Email, Price_Target, Alert_Active, Time_Created, Last_Checked)
    VALUES ('lvnlearn@gmail.com', 2000, TRUE, UNIX_TIMESTAMP() * 1000, UNIX_TIMESTAMP() * 1000); ''')
    
    cursor.execute('''SELECT * FROM Alerts_High;''')
    connection.commit()
    
    #careful here. Make sure that row is valid or function will time out. 
    for row in cursor:
        print(row)
        logger.info(row)
            
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Initializing GoldWatch',
                           
                           })
        
    }
