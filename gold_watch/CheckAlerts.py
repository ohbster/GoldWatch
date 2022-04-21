#writen by Obijah <ohbster@protonmail.com>
#https://github.com/ohbster/GoldWatch/

from get_connection import *
import logging
import json

connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Description: This function creates a list of all alerts that have been triggered and 
sends them to SQS to be process (Email delivery, etc)

How: 
1) First it selects all the currently active alerts in Alerts table.
2) Then it takes not of the oldest active alert by copying the Last_Checked attribute.
   By using last checked instead of Time_Created it avoids doing necessary repeat work
   as it will only evaluate each alert to each entry in Historical_Data once and only one
   time.
3) Next, it selects all the historical data in descending order from most recent that 
   were created after the oldest active alert. This is avoid processing any data that 
   is A) created before any alerts were created and B)Already evaulated against the alert
   This avoids unnecessary work
4) In get_trigger_list, a variable highest_price is initiated to the most recent spot
   price in data_list (from Historical_Data table). Since the data_list and alert_list
   are in chronological order from newer to older, keeping track of the highest price 
   is a useful since we will know any any target_price that is lower and older
   has been hit.
5) The first part of the get_trigger_list main loop compares the currently evaulated
   data_point (each tuple in Historical_Data) to keep track of the highest price.  
6) 


'''

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



def lambda_handler(context, event):
    cursor = connection.cursor()
    count = 0
            
    #get all alerts ordered by descending last_checked
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
    data_list = cursor.fetchall()
    if data_list is None:
        print("No results")
        
    #***************    
    #***DEBUGGING***
    #*************** 
    else:
        print("Data List: ")
        for entry in data_list:
            print(f"{entry[PRICE]},{entry[TIME_STAMP]}\n")
            #Sort the results by price
            #Sort the alerts by oldest first. If oldies has not been triggered. Go to next oldest 
            #skip unnecessary prices(older timestamps)
            #if a price in results is greater than target price in alerts list and happened after
            #the alert was created then trigger alert
            #- Trigger the alert. Remove alert from results
            #if not go to next price
            #- Since highest price triggered, we no all other
    
    #make sure to update all last checked values for each alert  
    if (len(data_list)) is 0:
        print("Empty datalist")
    elif (len(alert_list)) is 0:
        print("Empty alert_list")
    else:
        triggers = get_trigger_list(data_list, alert_list)
        
        #check if the function returned any alerts to trigger
        if triggers is None:
            print("No alerts were triggered")
        else:
            for trigger in triggers:
                print(f'Target reached: {trigger[PRICE_TARGET]}:{trigger[LAST_CHECKED]}')
        
    return{ "statusCode": 200,
           "body": json.dumps({
               "message" : f"{count} Alerts triggered",
               
               })
        
      
        }
#this function is for the high alerts

def get_trigger_list(_data_list, _alert_list):
    #get the most recent spot data_point from datalist
    #test lists are greater than length 0
    highest_price = _data_list[0][PRICE] 
    trigger_list = []
    ctr = 0 #counter used to iterate through _alert_list
    
    for data_point in _data_list: #Do this until _alert_list[ctr][lastchecked]. Then untab sections below 
        if float(data_point[PRICE]) > float(highest_price):
            #check for a new highest price
            highest_price = data_point[PRICE]
        
        #-----> Tab Over          
        #track of alerts
        #check if most recent spot data_point is after an alert has been created
        #go next in _alert_list. alert is too recent to have been triggered
        while(ctr < len(_alert_list)) and (int(data_point[TIME_STAMP]) < int(_alert_list[ctr][LAST_CHECKED])):
            #update the Last_Checked attribute to avoid "double dipping" historic data 
            #next time CheckAlerts gets triggered
            '''Cant assign tuples'''
            '''Add to a list or SQL'''
            #_alert_list[ctr][LAST_CHECKED] = data_point[TIME_STAMP]
            ctr += 1           
        while (ctr < len(_alert_list)) and (int(data_point[TIME_STAMP]) > int(_alert_list[ctr][LAST_CHECKED])):
            #if target price has been reached
            if float(highest_price) > float(_alert_list[ctr][PRICE_TARGET]):
                #add this alert to the trigger
                trigger_list.append(_alert_list[ctr])
                #deactivate the alert
                '''Cant assign tuples'''
                '''Add to a list or to SQL'''
                #_alert_list[ctr][ALERT_ACTIVE] = 0 
                #check the next alert
                '''Cant assign tuples'''
                '''Add to a list or to SQL'''
                #_alert_list[ctr][LAST_CHECKED] = data_point[TIME_STAMP]
            #else:
                #next(data_point)
            ctr += 1
            
    #Must update alert table rows with new Last_Checked values. 
    #Also send all alerts that need to be triggered to SQS for processing.
            
            
        return trigger_list   