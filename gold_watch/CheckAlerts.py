from get_connection import *
import logging
import json

connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def lambda_handler(context, event):
    cursor = connection.cursor()
    count = 0
    
    #get oldest alert from tables
    cursor.execute("SELECT MIN(Last_Checked) FROM Alerts_High WHERE Alert_Active = TRUE;")
    connection.commit()
    row = cursor.fetchone()
    if row is None:
        start_point = 0
    else:
        start_point = int(row[0])
        
    #get all price data after start_point (starting from where last check ended)
    cursor.execute(f'''SELECT Price,Time_Stamp FROM Historical_Data
    WHERE Time_stamp > {start_point}    
    ;''')
    connection.commit()
    results = cursor.fetchall()
    if results is None:
        print("No results")
    else:
        for entry in results:
            print(f"{entry[0]},{entry[1]}\n")
            #Sort the results by price
            #Sort the alerts by oldest first. If oldies has not been triggered. Go to next oldest 
            #skip unnecessary prices(older timestamps)
            #maybe shard by grouping Time_Created alerts together
            #if a price in results is greater than target price in alerts list and happened after
            #the alert was created then trigger alert
            #- Trigger the alert. Remove alert from results
            #if not go to next price
            #- Since highest price triggered, we no all other
    
    return{ "statusCode": 200,
           "body": json.dumps({
               "message" : f"{count} Alerts triggered",
               
               })
        
      
        }
