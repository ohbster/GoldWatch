from get_parameter import *
from botocore.exceptions import ClientError
import pymysql


def get_connection():
    client = boto3.client('ssm')
    
    #get database connection details from Parameter Store
    params = client.get_parameters(
        Names=[
            'gw-dbaddr',
            'gw-dbname',
            'gw-dbuser',
            'gw-dbport',
            'gw-dbpass'
            ], WithDecryption=True
        
        )
    
    #get_parameters() does not return them in order.
    #This is a workaround to avoid potentially exposing db password 
    #Need to match the 'Name' key to correct variable.
    #Steps: 
    #1. Iterate through list
    #2. If 'Name' matches a case, apply 'Value' to a variable.
    
    for x in params['Parameters']:
    
        if x['Name'] == 'gw-dbaddr':
            rds_host = x['Value']
        
        elif x['Name'] == 'gw-dbname':
            db_name = x['Value']
            
        elif x['Name'] == 'gw-dbuser':
            username = x['Value']
        
        elif x['Name'] == 'gw-dbpass':
            password = x['Value']
            
        elif x['Name'] == 'gw-dbport':
            rds_port = x['Value']
            
    return pymysql.connect(host=rds_host, user=username, password=password, db=db_name)

