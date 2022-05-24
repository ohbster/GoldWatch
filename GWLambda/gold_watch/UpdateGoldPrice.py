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
from get_connection import *
import pymysql

connection = get_connection()
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

    #get the most recent time_stamp in Historical_Data and use as point
    #to continue adding data.
    cursor.execute('''SELECT MAX(Time_Stamp) FROM Historical_Data;''')
    connection.commit()
    row = cursor.fetchone() #should only be one row from using MAX
    if row[0] is None:
        last_time_stamp = 0
    else:
        last_time_stamp = int(row[0])

    #Statement to insert historical data into table
    insert_statement = "INSERT INTO Historical_Data (Price, Time_Stamp) VALUES "
    values = ""


    #find the 24hour low, high, and current price
    for entry in price_data:
        cur_price = float(entry["price"])
        if cur_price > daily_high:
            daily_high = cur_price
        elif cur_price < daily_low:
            daily_low = cur_price
        #test if entry timestamp is greatter than time_stamp
        #if so add to insert statement

        if (int(entry["timestamp"]) > last_time_stamp) :
            values += f'''({entry["price"]},{entry["timestamp"]})'''
            #If the current entry is not the last, insert a comma between values
            if entry["timestamp"] != price_data[-1]["timestamp"] :
                values += ','
    #make sure values is not null
    if values == "":
        #do nothing
        print("No new data to insert to Historic table")
    else:
        values += ';'
        hd_sql  = insert_statement + values
        print (hd_sql)
        cursor.execute(hd_sql)
        connection.commit()

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
               "sql" : f"sql = {sql}",
               "day" : f"day = {day}"
               })


        }



#assert that price is not None

#testing code

#print(f'price_data is of type {type(price_data)}')
#print(f'price_data[1] is of type {type(price_data[1])}')

#for price in price_data:

#print(price_data)
