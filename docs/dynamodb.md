1. Upload data file [`foodorder.json`](../DynamoDBSetup/foodorder.json) to S3 bucket (e.g. imagesforwebsite) present in acd2022-serverless-workshop/DynamoDBSetup/
2. Now, to create a new table including the data in step-1, go the Dynamo DB Dashboard and choose "imports from S3"
3. Provide the URI of file in Source: s3://imagesforwebsite/foodorder.json
4. Provide Table name as: `foodorder`
5. Define Partition Key: ID
6. Define Sort Key: Type
7. Create table using Default settings