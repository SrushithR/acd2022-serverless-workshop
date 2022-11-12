## Setting up EventBridge

EventBridge has become an integral part of Serverless applications. In this section we will see how to create Event bus, Event Rules and integrate them with the following microservices:

1. [`restaurants_service`](../EventBridgeSetup/restaurants.py) - this microservice simulates the functionality of a restaurant, accepts orders and publishes a message (`Order Accepted`) to the event bus, which will be picked up the delivery and notification microservices
2. [`delivery service`](../EventBridgeSetup/delivery.py) - this microservice simulates the functionality of delivering the order to the customer's location, and publishes a message (`Order Delivered`) to the event bus, which will be picked up the notification microservice
3. [`notifications_service`](../EventBridgeSetup/notifications.py) - this microservice will help in sending WebSocket messages to the client using the API Gateway client of `boto3`

Create the above 3 lambda functions, which will be integrated with event rules in the following steps

### Steps to create an Event Bus

Navigate to the `EventBridge` service on the AWS console and perform the following steps to create an event bus:

1. Select `Event buses` on the left nav bar
2. Click on `Create event bus` to create a new event bus and provide a name for the same. Ex `food-app-bus` and leave the defaults for the rest of the things

### Steps to create Event Rules

As a part of our application, we will be creating 3 rules:

1. `OrderPlacedRule` - this rule will trigger the `restaurants` microservice to notify the restaurant that an order has been placed and the restaurant needs to accept and process the same.
2. `OrderAcceptedRule` - this rule will trigger the `delivery` microservice to start the delivery partner assignment and the delivery process. It will also trigger the `notifications` microservice to deliver the `Order Accepted` message to the client
3. `OrderDeliveredRule` - this rule will trigger the `notifications` microservice to delivery `Order Delivered` message to the client

Navigate to the `Event Rules` section on the left nav bar of the `EventBridge` console and perform the following steps to create event rules:

Select the event bus that was created in the previous section and click on `Create Rule` to create the following rules:

   1. Step 1 (Define rule detail) - Provide a name for the rule, `order_placed` and click on `Next`
   2. Step 2 (Build event pattern):
      1. Select `Other` as the `Event Source` to indicate that custom events will be used to push messages to the bus
      2. Add the following JSON to the `Event Pattern` section and click on `Next`:
         ```json
         {
           "detail-type": ["order_placed"],
           "source": ["custom.food_app"]
         }
         ```
   3. Step 3 (Select Targets):
      1. Select `AWS service` as the target and chose `Lambda function` from the dropdown list
      2. Select the `restaurants_service` lambda function that was created above and click on `Next`
   4. Step 4 (Configure Tags) - you can provide any tags if needed or can skip and click on `Next`
   5. Step 5 (Review and Create) - review all the configurations created in the previous steps and click on `Create Rule`

Repeat the above steps to create 2 more rules:

`Order Accepted Rule` with the following config:

1. `Event Pattern`:

```json
{
  "detail-type": ["order_accepted"],
  "source": ["custom.food_app"]
}
```
2. Two target lambda functions - `delivery_service` and `notification_service`

`Order Delivered Rule` with the following config:

1. `Event Pattern`:

```json
{
  "detail-type": ["order_delivered"],
  "source": ["custom.food_app"]
}
```

2. Target lambda - `notifications_service`

### Update Lambda Function Config

Create the following 2 environment variables in the `Configuration` section:

1. `WEBSOCKET_DOMAIN` - the websocket domain created as a part of the WebSockets section
2. `EVENT_BUS_NAME` - the name of the event bus created in the above step

### Testing

Navigate to the `Event Bus` on the left nav bar and click on `Send Events` and:

1. Select the event bus created above
2. Add the event source - `custom.food_app`
3. Add the detail type as `order_placed`
4. Add the following event detail:

```json

```