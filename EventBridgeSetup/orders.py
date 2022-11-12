import os
import json
import boto3
from datetime import datetime
from constants import ORDER_STATUSES

EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]


client = boto3.client("events")
ddb_client = boto3.resource("dynamodb")
table = ddb_client.Table("foodorder")


def lambda_handler(event, context):
    print("input to the lambda function", event)
    order_id = "OR00" + context.aws_request_id
    id = "A00" + context.aws_request_id
    table.put_item(
        Item={
            "ID": id,
            "restaurant_id": event["restaurant_id"],
            "order_amount": event["order_amount"],
            "order_discount": event["order_discount"],
            "order_amount_final": event["order_amount_final"],
            "items": event["items"],
            "Type": "Order",
            "customer_mobile": event["customer_mobile"],
            "order_status": "Order Placed",
            "order_id": order_id,
            "menu_id": event["menu_id"],
            "customer_name": event["customer_name"],
            "order_placed_at": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        }
    )

    order_details = {
        "order_id": id,
        "order_status": ORDER_STATUSES["ORDER_PLACED"],
        "user_id": event["user_id"],
    }

    response = client.put_events(
        Entries=[
            {
                "Time": datetime.now(),
                "Source": "custom.food_app",
                "DetailType": "order_placed",
                "Detail": json.dumps(order_details),
                "EventBusName": EVENT_BUS_NAME,
            },
        ]
    )

    print(response)
