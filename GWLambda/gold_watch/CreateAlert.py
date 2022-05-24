#This function creates an entry in either alerthigh or alertlow table.
#only allow one active alert per email per table
import json
import boto3



def lambda_handler(event,context):


  
    return {
        "status":200,
        "body":json.dumps({
            #"event":json.dumps(event)
            "message":"Testing123"
            })
            
        }