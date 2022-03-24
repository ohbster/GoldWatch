import json
import sys
import os
import logging
import pymysql
import boto3
from botocore.exceptions import ClientError

def get_parameter(parameter_name, with_decryption):
    ssm_client = boto3.client('ssm')
    
    try:
        result = ssm_client.get_parameter(
            Name=parameter_name,
            WithDecryption=with_decryption
            )
    except ClientError as e:
        logging.error(e)
        return None
    return result

rds_host = "goldwatchmysql.csdlsad8yvs8.us-east-1.rds.amazonaws.com"
#user = rds_config.db_username
#password = rds_config.db_password
#db_name = rds_config.db_name
db_name = (get_parameter('gw-dbname', False))['Parameter']['Value']
user = (get_parameter('gw-dbuser', False))['Parameter']['Value']
password = (get_parameter('gw-dbpass', True))['Parameter']['Value']

connection = pymysql.connect(host=rds_host, user=user, passwd=password, db=db_name)




def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS GoldPrice(
    Day DATE,
    High REAL,
    Low REAL,
    Current REAL
     
    );
    ''')
    cursor.execute('''INSERT INTO GoldPrice (Day, High, Low, Current)
    VALUES (0000-00-00, 0.00, 0.00, 0.00);
    ''')
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Initializing GoldWatch',
                           'db_name': f"{db_name}",
                           'db_user': f"{user}",
                           'rds_host': f"{rds_host}"
                           })
        
    }
