import json
import boto3
import datetime
def lambda_handler(event, context):
    print(type(event))
    print(event)
    print("Event json %s" % json.dumps(event))
    print("Context %s" % context)
    print("Restaurant_id %s" %event['restaurant_id'])
    
    client = boto3.resource('dynamodb')
    table = client.Table('foodorder')
    eventDateTime = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    published = False
    
    response = table.put_item(
        Item = {
            'ID': "A00" + context.aws_request_id,
            'restaurant_id': event['restaurant_id'],
            'order_amount': event['order_amount'],
			'order_discount': event['order_discount'],
			'order_amount_final': event['order_amount_final'],
			'items': event['items'],
			'Type': "Order",
			'customer_mobile': event['customer_mobile'],
			'order_status': "Order Placed",
			'order_id': "OR00" + context.aws_request_id,
			'menu_id': event['menu_id'],
			'customer_name': event['customer_name'],			
            'order_placed_at': eventDateTime,
            }
    )
    
    return {
        'statusCode': response['ResponseMetadata']['HTTPStatusCode'],
        'body': 'Record ' + context.aws_request_id + ' added'
        }
		
