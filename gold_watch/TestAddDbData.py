from get_connection import *
import logging
import json

connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(context, event):
    #insert values into Alerts_High
    cursor = connection.cursor()
    
        
    cursor.execute('TRUNCATE TABLE Alerts_High;')
    sql = '''INSERT INTO Alerts_High 
    (Email, Price_Target, Time_Created, Last_Checked)
    VALUES 
    ('goldwatchtest001@mailinator.com', 1930.00, 0, 1650401244631), 
    ('goldwatchtest002@mailinator.com', 2020.00, 0, 1650401934910),
    ('goldwatchtest003@mailinator.com', 1980.00, 0, 1650405775114),
    ('goldwatchtest004@mailinator.com', 2010.00, 0, 1650406074791)
  
    ; '''
    cursor.execute(sql)
    connection.commit()
    
    return{ "statusCode": 200,
           "body": json.dumps({
               "sql" : f"sql = {sql}",
               
               })
        
      
        }