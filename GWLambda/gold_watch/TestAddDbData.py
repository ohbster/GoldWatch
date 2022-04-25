from get_connection import *
import logging
import json

connection = get_connection()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(context, event):
    #insert values into Alerts_High
    cursor = connection.cursor()
    
    #cursor.execute('''DROP TABLE IF EXISTS Alerts_Low;''')
    #cursor.execute('''DROP TABLE IF EXISTS Alerts_High;''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_Low(
    Email VARCHAR(320) NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1,
    Time_Created BIGINT UNSIGNED NOT NULL,
    Last_Checked BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (Email, Time_Created)
    );
    ''')
    
    #Alerts if price goes above a certain target
    cursor.execute('''CREATE TABLE IF NOT EXISTS Alerts_High(
    Email VARCHAR(320) NOT NULL,
    Price_Target REAL NOT NULL,
    Alert_Active BOOLEAN DEFAULT 1,
    Time_Created BIGINT UNSIGNED NOT NULL,
    Last_Checked BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (Email, Time_Created)
    );    
    ''')
    
        
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
    
    sql = '''UPDATE Alerts_High
    SET Price_Target = (CASE WHEN Email = 'goldwatchtest002@mailinator.com' AND TIME_CREATED = 0 THEN 1999.00
                        WHEN Email = 'goldwatchtest004@mailinator.com' THEN 2000.00
                        ELSE Price_Target
                        END),
        Time_Created = 1
    ;''' #The ELSE Price_Target makes sure the update default to the original value instead of putting null values 
    #where the case doesn't match.
    cursor.execute(sql)
    connection.commit()
    
    cursor.execute('''SELECT * FROM Alerts_High    
    ;''')
    connection.commit()
    results = cursor.fetchall()
    for result in results:
        print(f"Email:{result[0]} | Price_Target:{result[1]} | Alert_Active:{result[2]} | Time_Created:{result[3]} | Last_checked:{result[4]}")
    
    
    return{ "statusCode": 200,
           "body": json.dumps({
               "sql" : f"sql = {sql}",
               
               })
        
      
        }