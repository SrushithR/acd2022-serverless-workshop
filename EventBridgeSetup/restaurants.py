import os
import json
import boto3
import time
from datetime import datetime
from constants import ORDER_STATUSES

EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]


client = boto3.client("events")


def lambda_function(event, context):
    print("Input", event)
    time.sleep(5)
    # TODO: Update DDB
    order_details = event["detail"]
    order_details = {
        "order_id": order_details["order_id"],
        "order_details": order_details["order_details"],
        "order_status": ORDER_STATUSES["ORDER_COMPLETED"],
        "user_id": order_details["user_id"],
    }

    response = client.put_events(
        Entries=[
            {
                "Time": datetime.now(),
                "Source": "custom.food_app",
                "DetailType": "order_completed",
                "Detail": json.dumps(order_details),
                "EventBusName": EVENT_BUS_NAME,
            },
        ]
    )

    print(response)
