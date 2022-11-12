import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
   print("Event json %s" % json.dumps(event))
   print("Context %s" % context)
   
   client = boto3.resource('dynamodb')
   table = client.Table('foodorder')

   restaurant_id = event['restaurant_id']
   
   print("Getting restaurant_id Filter %s" % restaurant_id)
   
   if not restaurant_id:
      print("Restaurant_id not passed, display all available Menus")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Menu') 
                     )
   else:
      print("Title is NOT empty")
      response = table.scan(
                     FilterExpression = Attr('Type').eq('Menu') & Attr('restaurant_id').eq(restaurant_id) 
                     )
   

   return response['Items']
  
