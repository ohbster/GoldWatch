import json
import sys
import os
import logging
import pymysql
import boto3
from botocore.exceptions import ClientError
from get_parameter import * 


rds_host = (get_parameter('gw-dbaddr', False))['Parameter']['Value']
rds_port = (get_parameter('gw-dbport', False))['Parameter']['Value']
db_name = (get_parameter('gw-dbname', False))['Parameter']['Value']
user = (get_parameter('gw-dbuser', False))['Parameter']['Value']
password = (get_parameter('gw-dbpass', True))['Parameter']['Value']

connection = pymysql.connect(host=rds_host, user=user, passwd=password, db=db_name)
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(event, context):
    print("Creating Table")
    cursor = connection.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS GoldPrice(
    Day DATE PRIMARY KEY NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Current REAL NOT NULL
    );
    ''')
    
    #Alerts if price goes below a target
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_Lower(
    Email VARCHAR(320) PRIMARY KEY NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1
    );
    ''')
    
    #Alerts if price goes above a certain target
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_Upper(
    Email VARCHAR(320) PRIMARY KEY NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1
    );    
    ''')
    cursor.execute('''INSERT INTO GoldPrice (Day, High, Low, Current)
    VALUES (0000-00-00, 0.00, 0.00, 0.00);
    ''')
    cursor.execute('''SELECT * FROM GoldPrice''')
    for row in cursor:
        print(row)
        logger.info(row)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Initializing GoldWatch',
                           'db_name': f"{db_name}",
                           'db_user': f"{user}",
                           'rds_host': f"{rds_host}"
                           })
        
    }
