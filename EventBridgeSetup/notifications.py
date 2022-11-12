import json
import os
import boto3
from boto3.dynamodb.conditions import Key

WEBSOCKET_DOMAIN = os.environ["WEBSOCKET_DOMAIN"]

websocket_connection_url = f"https://{WEBSOCKET_DOMAIN}/dev"

client = boto3.client("apigatewaymanagementapi", endpoint_url=websocket_connection_url)
dynamodb_resource = boto3.resource("dynamodb")
connection_manager = dynamodb_resource.Table("connection-manager")


def get_connection_id(user_id):
    connection_details = connection_manager.query(
        IndexName="UserIdIndex", KeyConditionExpression=Key("user_id").eq(user_id)
    )
    print("connection_details", connection_details)
    return connection_details["Items"][0]["connection_id"]


def lambda_handler(event, context):
    print("Input", event)
    event_details = event["detail"]
    user_id = event_details["user_id"]
    del event_details["user_id"]
    connection_id = get_connection_id(user_id)

    response = client.post_to_connection(
        Data=json.dumps(event_details), ConnectionId=connection_id
    )
    print(response)
