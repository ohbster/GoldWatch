#This function retrieves price and timestamp data from api.metals.live.
#Returns the current daily_low, daily_high, and current price.

#optionally, draw a graph (Line or candlestick) with all the data returned 


#this function should run every 5 mins, or 12 times every hour
#288 times a day, or ~8640 times a month

import json
import requests


def lambda_handler(event, context):


    response = requests.get("http://api.metals.live/v1/spot/gold")
    price_data = json.loads(response.text)
    #price_data = None
    
    #need to verify data is good
    

    if price_data is None:
        return {"statusCode": 200,
                "body": json.dumps({
                    "message": "Price data is currently unavailable",
                    
                    }
                    ),
            
            }
    
        
    daily_low = float(price_data[0]["price"])
    daily_high = float(price_data[0]["price"]) 
    cur_price = float(price_data[0]["price"])
    
    
    for entry in price_data:
        cur_price = float(entry["price"])
        if cur_price > daily_high:
            daily_high = cur_price
        elif cur_price < daily_low:
            daily_low = cur_price
    
    return{ "statusCode": 200,
           "body": json.dumps({
               "message": f"current price = {cur_price}" \
               f" highest price = {daily_high}",
               "daily_high": f"{daily_high}",
               "daily_low": f"{daily_low}",
               "cur_price": f"{cur_price}"
               })
        
        
        }
"""    
    print(f"highest price: {daily_high}")
    print(f"lowest price: {daily_low}")
    print(f"current price: {cur_price}")
"""

#assert that price is not None

#testing code

#print(f'price_data is of type {type(price_data)}')
#print(f'price_data[1] is of type {type(price_data[1])}')

#for price in price_data:
    
#print(price_data)