import os
import json
import boto3
from datetime import datetime
from constants import ORDER_STATUSES

EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]


client = boto3.client("events")


def lambda_function(event, context):
    order_details = {
        "order_id": event["order_id"],
        "order_details": [{"item_id": 1234}],
        "order_status": ORDER_STATUSES["ORDER_PLACED"],
        "user_id": event["user_id"]
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
