import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
   print("Event json %s" % json.dumps(event))
   print("Context %s" % context)
   
   client = boto3.resource('dynamodb')
   table = client.Table('foodorder')
   
   customer_mobile = event['customer_mobile']
   
   print("Getting Customer Mobile Filter %s" % customer_mobile)
   
   if not customer_mobile:
      print("Title is empty")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Order')
                     )
   else:
      print("Title is NOT empty")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Order') & Attr('customer_mobile').eq(customer_mobile) 
                     )

   return response['Items']
