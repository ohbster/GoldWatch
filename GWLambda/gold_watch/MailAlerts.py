import os
import boto3
from botocore.exceptions import ClientError
import json
from receive_sqs import *


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event,context):
    
    QUEUE_NAME='GoldWatchAlertTriggerQueue'
    
    #Alert Trigger queue
    messages = receive_sqs(QUEUE_NAME)
    logging.info(messages)
    if messages is None or len(messages) is 0 :
        print("No messages in queue")
        
    else:
        for message in messages['Messages']:
            body = message['Body']
            receipt_handle = message['ReceiptHandle']
            
            print(f'Body = {body}')
            print(f'Deleting message {receipt_handle} from queue')
            delete_sqs(QUEUE_NAME, receipt_handle)
    
    SENDER = "noreply@goldwatch.link"
    RECIPIENT = "goldwatchtest1@mailinator.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "SES Test"
    CHARSET = "UTF-8"
    
    client = boto3.client('ses',region_name=AWS_REGION)
    
    td = {
                "name":"ohbster", 
                "pricetarget":"2001"
            }
    
    try:
        response = client.send_templated_email(
            Source=SENDER,
            Destination={
                'ToAddresses':[
                    RECIPIENT,
                ],
            },
            Template ='AlertTemplate',
            #TemplateData = json.dumps(td),
            TemplateData = '{ \"name\":\"ohbster\",\"pricetarget\":\"2001\" }',
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