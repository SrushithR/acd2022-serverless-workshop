import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
   print("Event json %s" % json.dumps(event))
   print("Context %s" % context)
   
   client = boto3.resource('dynamodb')
   table = client.Table('foodorder')
   
   menu_id = event['menu_id']
   
   print("Getting Menu_id Filter %s" % menu_id)
   
   if not menu_id:
      print("Title is empty")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Item')
                     )
   else:
      print("Title is NOT empty")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Item') & Attr('menu_id').eq(menu_id) 
                     )

   return response['Items']
  

