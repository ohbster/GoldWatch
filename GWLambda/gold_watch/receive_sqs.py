import boto3
import logging
import json
from botocore.exceptions import ClientError

def receive_sqs (queue_name):
    client = boto3.client('sqs', region_name = 'us-east-1')
    sqs_queue_url = client.get_queue_url(QueueName=queue_name)['QueueUrl']
    
    try:
        response = client.receive_message(QueueUrl=sqs_queue_url)
    except ClientError as e:
        logging.error(e)
        return None
    return response

def delete_sqs(queue_name, receipt_handle):
    client = boto3.client('sqs', region_name = 'us-east-1')
    sqs_queue_url = client.get_queue_url(QueueName=queue_name)['QueueUrl']
    
    try:
        response = client.delete_message(QueueUrl=sqs_queue_url, ReceiptHandle=receipt_handle)
    except ClientError as e:
        logging.error(e)
        return None
    print(f"response = {response}")
    return response
        