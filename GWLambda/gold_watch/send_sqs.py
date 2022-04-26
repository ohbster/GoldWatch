import boto3
import logging
import json
from botocore.exceptions import ClientError


def send_sqs(queue_name,message):
    # Create SQS client
    sqs = boto3.client('sqs')
    
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    
    #convert dictionary to json
    data = json.dumps(message)
    
    # Send message to SQS queue
    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageBody=(data)
        )
    except ClientError as e:
        logging.error(e)
        return None
        
    return response
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #client = boto3.client('sqs')
    #sqs_queue_url = client.get_queue_url(QueueName=queue_name)['QueueUrl']
    
    #try:
    #    msg = client.send_message(QueueUrl=sqs_queue_url, MessageBody=json.dumps(msg_body))
    #except ClientError as e:
    #    logging.error(e)
    #    return None
    #return msg