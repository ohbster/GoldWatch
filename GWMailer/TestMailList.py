import boto3

client = boto3.client('sesv2')

create_contact()
response = client.create_contact(
    ContactListName='Alerts',
    EmailAddress='lvnlearn@gmail.com',
    TopicPreferences=[
        {
            'TopicName': 'Added to alert list',
            'SubscriptionStatus': 'OPT_IN'|'OPT_OUT'
        },
    ],
    UnsubscribeAll=True|False,
    AttributesData='string'
)

create_contact_list()

response = client.create_contact_list(
    ContactListName='Alerts',
    Topics=[
        {
            'TopicName': 'AlertTriggeredList',
            'DisplayName': 'Alert Triggered',
            'Description': 'A price alert has been triggered',
            'DefaultSubscriptionStatus': 'OPT_IN'|'OPT_OUT'
        },
    ],
    Description='string',
    Tags=[
        {
            'Key': 'Name',
            'Value': 'Alert Triggered List'
        },
    ]
)