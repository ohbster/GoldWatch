import os
import boto3
from botocore.exceptions import ClientError
import json
from receive_sqs import *
from datetime import datetime


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event,context):
       
    print("Logging Event")
    print(json.dumps(event))
    logger.info(json.dumps(event))
    
    #testDict = json.dump(event['Records'][0]['body'])

    alerts = event['Records'][0]['body']
    #print(f"Alerts is of type {type(alerts)}")
    
    alerts = json.loads(alerts)
    #print(f"alerts = {alerts}")
   
    SENDER = "noreply@goldwatch.link"
    #RECIPIENT = "goldwatchtest1@mailinator.com"
    AWS_REGION = "us-east-1"
    #SUBJECT = "SES Test"
    #CHARSET = "UTF-8"
       
    client = boto3.client('ses',region_name=AWS_REGION)
    
    
    for alert in alerts:
        
        
    
        dt = datetime.fromtimestamp(alert['TimeCreated'])
        ################################
        #Debuugging delete me
        ################################
        print(f"TimeCreated = {alert['TimeCreated']}")
        print(f"dt = {dt.strftime('%x %X')}")
    
     
        try:
            response = client.send_templated_email(
                Source=SENDER,
                Destination={
                    'ToAddresses':[
                        alert['Email']
                    ],
                },
                Template ='AlertTemplate',
                TemplateData = '{ \"time_created\":' + 
                f"\"{dt.strftime('%x %X')}\"" + 
                ',\"price_target\":' + f"{alert['PriceTarget']}" + '}',
               
                ConfigurationSetName = 'FailureToSend'
            )
            
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response)
    
    return { "statusCode":"200",
            "body":json.dumps({
                "message":"test123"
                })}