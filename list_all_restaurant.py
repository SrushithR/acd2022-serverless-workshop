import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
   print("Event json %s" % json.dumps(event))
   print("Context %s" % context)
   
   client = boto3.resource('dynamodb')
   table = client.Table('foodorder')
   

   response = table.scan(
                  FilterExpression = Attr('Type').eq('Restaurant')
                  )

   return response['Items']
  
