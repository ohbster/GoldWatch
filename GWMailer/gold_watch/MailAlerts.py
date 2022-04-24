import os
import boto3
from botocore.exceptions import ClientError
import json

def lambda_handler(event,context):
    
    
    SENDER = "noreply@goldwatch.link"
    RECIPIENT = "lvnlearn@gmail.com"
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