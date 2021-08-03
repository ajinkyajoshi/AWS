import boto3
from datetime import date
import json

iam_client = boto3.client('iam')
sns_client = boto3.client('sns')

user = '<user_name>'
key_validity_days = 84
sns_topic_arn = 'arn:aws:sns:us-east-1:XXXXXXXXXXXX:NotifyMe'
message = "Please rorate the keys....Access key age is: "

user_response = iam_client.list_access_keys(UserName=user)
user_accesskeydate = user_response['AccessKeyMetadata'][0]['CreateDate'].date()
user_currentdate = date.today()
user_active_days = user_currentdate - user_accesskeydate
print (user_active_days.days)

if user_active_days.days > key_validity_days:
    print("Rotate access keys")
    response = sns_client.publish(
            TargetArn=sns_topic_arn,
            Message=json.dumps({'default': json.dumps(message+str(user_active_days.days))}),
            Subject='Alert ! Rotate access keys for user '+ user,
            MessageStructure='json'
    )
else:
    print("")
