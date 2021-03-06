#writen by Obijah <ohbster@protonmail.com>
#https://github.com/ohbster/GoldWatch/

from get_connection import *
import time
import logging
import json
import boto3
from send_sqs import send_sqs

connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
CheckAlerts
by Obijah <ohbster@protonmail.com>

Description: This function creates a list of all alerts that have been triggered and
sends them to SQS to be process (Email delivery, etc)

How:
1) First it selects all the currently active alerts in Alerts table.
2) Then it takes note of the oldest active alert by copying the Last_Checked attribute.
   By using last checked instead of Time_Created it avoids doing necessary repeat work
   as it will only evaluate each alert to each entry in Historical_Data once and only one
   time. After the alerts are checked, there Last_Checked value will be updated with a
   recent timestamp where it will continue during the next scan, ignoring older data.
3) Next, it selects all the historical data in descending order from most recent that
   were created after the oldest active alert. This is avoid processing any data that
   is A) created before any alerts were created and B)Already evaulated against the alert
   This avoids unnecessary work
4) In get_trigger_list, a variable highest_price is initiated to -1. Since the data_list and alert_list
   are in chronological order from newer to older, keeping track of the highest price
   is a useful since we will know any target_price has been hit if it is lower and older than a spot
   price.
5) The first part of the get_trigger_list main loop iterates through each alert in _alert_list
6) The next inner while loop ensure that only spot prices newer than the alert will trigger an alert.
   If the spot price is older, the outer loop will select and older alert to evaluate.
7) If the spot price is valid, check to see if it's price is the current highest price. If so, assign it to
   highest_price
8) Next, check to see if the highest_price is greater than the alert. If so, add the alert to the trigger_list
   (We know the spot price happened after the alert because they are both in chronological order)
9) If the price is not greater, then go to the next spot price in _spot_prices by increasing counter 'ctr'.
   First check that increasing will not go out of bounds.
10)If for some reason, increasing ctr will go out of bounds in _spot_prices, then this is the last spot price.
   Compare this price to the rest of the alerts and end the loop.
11)Update all the Last_Checked values.
12)Any alert that was triggered needs to be deactivated by switching ACTIVE to 0
13)Return the trigger list

'''

QUEUE_NAME = 'GoldWatchAlertTriggerQueue'

##########
#SCHEMA
##########
#this is to make the code easier to read and maintain if I change the database later
#Alerts_High
PRICE_TARGET = 0
LAST_CHECKED = 1
EMAIL = 2
ALERT_ACTIVE = 3
TIME_CREATED = 4

#Historical_Data
PRICE = 0
TIME_STAMP = 1

#get_trigger_list modes
HI = 2
LO = 1

def lambda_handler(event, context):
    cursor = connection.cursor()

    #######################
    #High alerts Populating
    #######################

    #get all high alerts ordered by descending last_checked
    cursor.execute('''SELECT Price_Target, Last_Checked, Email, Alert_Active, Time_Created
    FROM Alerts_High
    WHERE Alert_Active = 1
    ORDER BY Last_Checked DESC; ''')
    connection.commit()
    alert_list = cursor.fetchall()

    if alert_list is None:
        print("No alerts active")
    #***************
    #***DEBUGGING***
    #***************
    else:
        for alert in alert_list:
            print(f'{alert[0]}, {alert[LAST_CHECKED]}')

        #get the oldest last_checked timestamp
        #this returns the last_checked timestamp of last alert in list (ordered from new to old)
        oldest_alert = alert_list[len(alert_list)-1][LAST_CHECKED]

        #get all price data after start_point (starting from where last check ended)
        cursor.execute(f'''SELECT Price,Time_Stamp FROM Historical_Data
        WHERE Time_stamp > {oldest_alert}
        ORDER BY Time_Stamp DESC
        ;''')
        connection.commit()
        spot_prices = cursor.fetchall()
        if spot_prices is None:
            print("No results")

        #################################################
        #Update Alert_High table and Send triggers to SQS
        #################################################
        if (len(spot_prices)) is 0:
            print("No new spot prices")
        elif (len(alert_list) is 0):
            print("Empty alert lists")
        else:
            #First Time_Stamp. Will update all Last_Checked values using this
            first_time_stamp = spot_prices[0][TIME_STAMP]
            #Make sure the alert list has data before trying to run get_trigger*()
            if len(alert_list):
                high_triggers = get_trigger_list(spot_prices, alert_list,mode=HI)
                if len(high_triggers):
                    #Must update alert table rows with new Last_Checked values.
                    sql = f'''UPDATE Alerts_High
                    SET Alert_Active = (CASE '''
                    #this will create a case for every triggered alert to deactivate them
                    for triggered in high_triggers:
                        #sql +=f''' WHEN Email = '{triggered[EMAIL]}' AND Time_Created = {triggered[TIME_CREATED]} THEN 0'''
                        sql +=f''' WHEN Email = '{triggered['Email']}' AND Time_Created = {triggered['TimeCreated']} THEN 0'''
                    sql +=(f''' ELSE Alert_Active
                    END),
                    Last_Checked = {first_time_stamp}
                    WHERE Alert_Active = 1
                    ;''')
                    cursor.execute(sql)
                    connection.commit()

                    response = send_sqs(QUEUE_NAME, high_triggers)
                    logger.info(response)

    ######################
    #Low alerts Populating
    ######################

    #get all low alerts ordered by descending last_checked
    cursor.execute('''SELECT Price_Target, Last_Checked, Email, Alert_Active, Time_Created
    FROM Alerts_Low
    WHERE Alert_Active = 1
    ORDER BY Last_Checked DESC; ''')
    connection.commit()
    alert_low_list = cursor.fetchall()

    if len(alert_low_list) is 0:
        print("No alerts active")

    else:
        for alert in alert_low_list:
            print(f'low alert: {alert[0]}, {alert[LAST_CHECKED]}')

        #get the oldest last_checked timestamp
        #this returns the last_checked timestamp of last alert in list (ordered from new to old)
        oldest_low_alert = alert_low_list[len(alert_low_list)-1][LAST_CHECKED]

        #get all price data after start_point (starting from where last check ended)
        cursor.execute(f'''SELECT Price,Time_Stamp FROM Historical_Data
        WHERE Time_stamp > {oldest_low_alert}
        ORDER BY Time_Stamp DESC
        ;''')
        connection.commit()
        spot_prices_low = cursor.fetchall()

        #################################################
        #Update Alert_Low table and Send triggers to SQS
        #################################################
        if (len(spot_prices_low)) is 0:
            print("No new low spot prices")
        elif (len(alert_low_list) is 0):
            print("Empty alert lists")
        else:
            if len(alert_low_list):
                low_triggers = get_trigger_list(spot_prices_low,alert_low_list, mode=LO)
                if len(low_triggers):
                    #Must update alert table rows with new Last_Checked values.
                    sql = f'''UPDATE Alerts_Low
                    SET Alert_Active = (CASE '''
                    #this will create a case for every triggered alert to deactivate them
                    for triggered in low_triggers:
                        sql +=f''' WHEN Email = '{triggered['Email']}' AND Time_Created = {triggered['TimeCreated']} THEN 0'''
                    sql +=(f''' ELSE Alert_Active
                    END),
                    Last_Checked = {first_time_stamp}
                    WHERE Alert_Active = 1
                    ;''')
                    cursor.execute(sql)
                    connection.commit()

                    response = send_sqs(QUEUE_NAME, low_triggers)
                    logger.info(response)

    return{ "statusCode": 200,
           "body": json.dumps({
               'body' : json.dumps(event),
               })
        }
#this function is for the high alerts
def get_trigger_list(_spot_prices, _alert_list, mode):
    #get the most recent spot price from spot_prices

    highest_price = -1
    highest_price_timestamp = 0 #May use this later
    lowest_price = int(_spot_prices[0][PRICE])
    #Return this list to handler
    trigger_list = []
    #internal list for updating tuples

    ctr = 0 #counter used to iterate through _alert_list

    for alert in _alert_list:
        #keep track of the starting spot price being process

        #make sure to only check alerts created (and by proxy, last checked) before the spot prices occur
        while (int(_spot_prices[ctr][TIME_STAMP]) > int(alert[LAST_CHECKED])):
            #Check if this spot price is the highest price scanned so far
            #if (spotprice > highest_price AND CHECKHI)
            if (int(_spot_prices[ctr][PRICE]) > highest_price) and mode is HI:
                highest_price = int(_spot_prices[ctr][PRICE])
                highest_price_timestamp = int(_spot_prices[ctr][TIME_STAMP])
            #if a higher price has happened  after the alert, trigger it. Then go next alert
            #if (spotprice < lowest_price AND CHECKLO)
            #(if highest_price > alert[Target] && CHECKHI) OR() lowest_price < lowalert[target] && CHECKLO
            if (int(_spot_prices[ctr][PRICE]) < lowest_price) and mode is LO:
                lowest_price = int(_spot_prices[ctr][PRICE])
                lowest_price_timestamp = int(_spot_prices[ctr][TIME_STAMP])

            if (lowest_price < int(alert[PRICE_TARGET]) and mode is LO) or \
            (highest_price > int(alert[PRICE_TARGET]) and mode is HI):
                #append dictionaries to the list
                trigger_list.append({'Email':alert[EMAIL],
                                     'PriceTarget':alert[PRICE_TARGET],
                                     'TimeCreated':alert[TIME_CREATED],
                                     'LastChecked':alert[LAST_CHECKED],
                                     'AlertActive':alert[ALERT_ACTIVE]})
                break
            #if not, then continue checking spot prices before alerts creation(/last checked)
            #prevent ctr from going out of range
            elif ctr < (len(_spot_prices)-1):
                ctr+=1
            #if for some reason, reached the end of spot prices with some alerts left. Just keep checking alerts
            else:
                #update_alerts_list.append([(alert[PRICE_TARGET],alert[LAST_CHECKED]), alert[EMAIL], alert[ALERT_ACTIVE],])
                break

    #Also send all alerts that need to be triggered to SQS for processing.
    #print(f"Highest price in data is :{highest_price}")
    return trigger_list
