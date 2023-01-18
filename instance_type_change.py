from boto3 import client
import boto3

ec2_event = boto3.client('ec2')

environment = "dev"
application = "dev1"
instance_type = "t2.micro"

custom_filter = [
        {
            'Name': "tag:" + "env",
            'Values':  [environment]
        },
        {
            'Name': "tag:" + "app",
            'Values':  [application]
        }
]


for page in client('ec2').get_paginator('describe_instances').paginate(Filters=custom_filter):
    for res in page['Reservations']:
        for inst in res['Instances']:
            try:
                if inst['State']['Name'] == 'running':
                    if inst['InstanceType'] != instance_type:
                        print(inst['InstanceId'] + " is in running state....Stopping the instance: "+ inst['InstanceId'] +"\n")
                        ec2_event.stop_instances(InstanceIds=[inst['InstanceId']])
                        waiter = ec2_event.get_waiter('instance_stopped')
                        waiter.wait(InstanceIds=[inst['InstanceId']])
                        print(inst['InstanceId']+ " is in stopped state....changing it's type to "+ instance_type +"\n")
                        ec2_event.modify_instance_attribute(InstanceId=inst['InstanceId'], Attribute='instanceType', Value=instance_type)
                        print(inst['InstanceId']+ " Instance type Changed.....\n")
                        print("Starting "+ inst['InstanceId']+"\n")
                        ec2_event.start_instances(InstanceIds=[inst['InstanceId']])
                        print("----------------------------------------------------------------------------------------------\n")
                    else:
                        print(inst['InstanceId']+ " Instance type is already changed to "+instance_type)
                        print("----------------------------------------------------------------------------------------------\n")
                elif inst['State']['Name'] == 'stopped':
                    if inst['InstanceType'] != instance_type:
                        print(inst['InstanceId']+ " is already stopped....changing it's type to "+ instance_type + "\n")
                        ec2_event.modify_instance_attribute(InstanceId=inst['InstanceId'], Attribute='instanceType', Value=instance_type)
                        print(inst['InstanceId']+ " Instance type Changed.....\n")
                        print("Starting "+ inst['InstanceId'] +"\n")
                        ec2_event.start_instances(InstanceIds=[inst['InstanceId']])
                        print("----------------------------------------------------------------------------------------------\n")
                    else:
                        print(inst['InstanceId']+ " Instance type is already changed to "+instance_type)
                        print("----------------------------------------------------------------------------------------------\n")
            except Exception as e:
                print("Unknown Error.... Please contact Admin !")
