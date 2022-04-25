import boto3
import logging
import json
from botocore.exceptions import ClientError


def send_sqs(queue_name,msg_body):
    client = boto3.client('sqs')
    sqs_queue_url = client.get_queue_url(QueueName=queue_name)['QueueUrl']
    
    try:
        msg = client.send_message(QueueUrl=sqs_queue_url, MessageBody=json.dumps(msg_body))
    except ClientError as e:
        logging.error(e)
        return None
    return msg