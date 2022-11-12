import os
import json
import boto3
import time
from datetime import datetime
from constants import ORDER_STATUSES

EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]


client = boto3.client("events")
ddb_client = boto3.resource("dynamodb")
table = ddb_client.Table("foodorder")


def lambda_handler(event, context):
    print("Input", event)
    time.sleep(10)

    order_details = event["detail"]
    order_id = order_details["order_id"]

    table.update_item(
        Key={"ID": order_id, "Type": "Order"},
        UpdateExpression="SET order_status= :var1, order_delivered_at= :var2",
        ExpressionAttributeValues={
            ":var1": ORDER_STATUSES["ORDER_DELIVERED"],
            ":var2": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        },
        ReturnValues="UPDATED_NEW",
    )

    order_details = {
        "order_id": order_details["order_id"],
        "order_status": ORDER_STATUSES["ORDER_DELIVERED"],
        "user_id": order_details["user_id"],
    }

    response = client.put_events(
        Entries=[
            {
                "Time": datetime.now(),
                "Source": "custom.food_app",
                "DetailType": "order_delivered",
                "Detail": json.dumps(order_details),
                "EventBusName": EVENT_BUS_NAME,
            },
        ]
    )

    print(response)
