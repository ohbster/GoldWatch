#This function retrieves price and timestamp data from api.metals.live.
#Returns the current daily_low, daily_high, and current price.

#optionally, draw a graph (Line or candlestick) with all the data returned 


#this function should run every 5 mins, or 12 times every hour
#288 times a day, or ~8640 times a month

import json
import requests
import datetime
import os
import boto3
import logging
from botocore.exceptions import ClientError
from get_parameter import *
import pymysql

client = boto3.client('ssm')

#get database connection details from Parameter Store
params = client.get_parameters(
    Names=[
        'gw-dbaddr',
        'gw-dbname',
        'gw-dbuser',
        'gw-dbport',
        'gw-dbpass'
        ], WithDecryption=True
    
    )

#get_parameters() does not return them in order.
#This is a workaround to avoid potentially exposing db password 
#Need to match the 'Name' key to correct variable.
#Steps: 
#1. Iterate through list
#2. If 'Name' matches a case, apply 'Value' to a variable.

for x in params['Parameters']:

    if x['Name'] == 'gw-dbaddr':
        rds_host = x['Value']
    
    elif x['Name'] == 'gw-dbname':
        db_name = x['Value']
        
    elif x['Name'] == 'gw-dbuser':
        username = x['Value']
    
    elif x['Name'] == 'gw-dbpass':
        password = x['Value']
        
    elif x['Name'] == 'gw-dbport':
        rds_port = x['Value'] 

connection = pymysql.connect(host=rds_host, user=username, password=password, db=db_name)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    cursor = connection.cursor()
    #get price data from public source
    response = requests.get("http://api.metals.live/v1/spot/gold")
    price_data = json.loads(response.text)

    #need to verify data is good
    if price_data is None:
        return {"statusCode": 200,
                "body": json.dumps({
                    "message": "Price data is currently unavailable",
                    
                    }
                    ),
            
        }
    
    #initialize variables (to set the low's and highs)    
    daily_low = float(price_data[0]["price"])
    daily_high = float(price_data[0]["price"]) 
    cur_price = float(price_data[0]["price"])
    day = datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    for entry in price_data:
        cur_price = float(entry["price"])
        if cur_price > daily_high:
            daily_high = cur_price
        elif cur_price < daily_low:
            daily_low = cur_price
            
            
    #update the daily row 
    sql = f'''INSERT INTO GoldPrice(Daystamp, High, Low, Current)
    VALUES ('{day}', {daily_high}, {daily_low}, {cur_price})
    ON DUPLICATE KEY UPDATE
    High = {daily_high}, Low = {daily_low}, Current = {cur_price};
    
    '''
    cursor.execute(sql)
    connection.commit()
    
    for row in cursor:
        print(row)
        logger.info(row)
    
    
    return{ "statusCode": 200,
           "body": json.dumps({
               "rds_host" : f"rds_host = {rds_host}",            
               "dbname" : f"dbname = {db_name}",
               "username" : f"dbuser = {username}",
               "day" : f"day = {day}"
               })
        
      
        }
    


#assert that price is not None

#testing code

#print(f'price_data is of type {type(price_data)}')
#print(f'price_data[1] is of type {type(price_data[1])}')

#for price in price_data:
    
#print(price_data)