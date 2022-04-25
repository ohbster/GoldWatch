import os
import boto3
from botocore.exceptions import ClientError
import json
from receive_sqs import *


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event,context):
    
    QUEUE_NAME='GoldWatchAlertTriggerQueue'
    
    # Create SQS client
    sqs = boto3.client('sqs')
    
    #queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
    queue_url = 'https://sqs.us-east-1.amazonaws.com/378576100664/GoldWatchAlertTriggerQueue'
    
    print("Logging Event")
    print(json.dumps(event))
    logger.info(json.dumps(event))
    '''    
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            #'SentTimestamp'
            'All'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    
    logger.info(json.dumps(response))

    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']
    
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Received and deleted message: %s' % message)
    '''  
    SENDER = "noreply@goldwatch.link"
    RECIPIENT = "goldwatchtest1@mailinator.com"
    AWS_REGION = "us-east-1"
    SUBJECT = "SES Test"
    CHARSET = "UTF-8"
    
    client = boto3.client('ses',region_name=AWS_REGION)
    
    td = {
                #"name":"ohbster",
                "name":f"{event}", 
                "pricetarget":"2001",
                #"Message ID":f"{event["
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
            #TemplateData = td,
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