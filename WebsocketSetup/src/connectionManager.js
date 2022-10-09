const aws = require("aws-sdk");
const { promisify } = require("util");

const ddb = new aws.DynamoDB.DocumentClient();

ddb.putPromise = promisify(ddb.put);
ddb.updatePromise = promisify(ddb.update);
ddb.getPromise = promisify(ddb.get);
ddb.deletePromise = promisify(ddb.delete);
ddb.queryPromise = promisify(ddb.query);

const { CONNECTION_TABLE_NAME } = process.env;
const GSI_NAME = "UserIdIndex";

const persist = async (connectionId, data) =>
  DDB.putItem({
    TableName: CONNECTION_STORE,
    Item: { connectionId, ...data }
  })

const remove = async connectionId =>
  DDB.deleteItem({
    TableName: CONNECTION_TABLE_NAME,
    Key: {connectionId}
  });

const getByUserId = async userId => {
  const connectionDetails = await DDB.queryItems({
    TableName: CONNECTION_TABLE_NAME,
    IndexName: GSI_NAME,
    KeyConditionExpression: "userId = :id",
    ExpressionAttributeValues: {":id": userId}
  });
  return connectionDetails.Items;
};

module.exports.ConnectionStore = { persist, remove, getByUserId };
