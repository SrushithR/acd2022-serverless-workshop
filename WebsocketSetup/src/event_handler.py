import boto3

dynamodb_resource = boto3.resource("dynamodb")
connection_manager = dynamodb_resource.Table("connection-manager")


def lambda_handler(event, context):
    print("Input to the lambda function", event)
    route = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]

    if route == "$connect":
        user_id = event["queryStringParameters"]["user_id"]
        print("Establishing connection")
        user_details = {"user_id": user_id, "connection_id": connection_id}
        connection_manager.put_item(Item=user_details)
        return {"statusCode": 200, "body": "Connection established successfully"}
    elif route == "$disconnect":
        print("Disconnecting")
        connection_manager.delete_item(Key={"connection_id": connection_id})
        return {"statusCode": 200, "body": "Connection removed successfully"}
    else:
        print("invalid route")
        return {"statusCode": 404, "body": "Invalid Route"}
