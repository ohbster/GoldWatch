import json
import datetime

def lambda_handler(event, context):
    d = datetime.datetime.now()
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "today is " + d.strftime("%A, %B %d %Y"),
            
            }),
        
        }