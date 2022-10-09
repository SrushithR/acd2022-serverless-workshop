const { ConnectionManager } = require("./connectionManager")

exports.eventHandler = async event => {
  console.log("Input:", event);

  const {
    requestContext: { connectionId, routeKey }
  } = event;

  switch (routeKey) {
    case "$connect":
      return ConnectionManager.makeConnection(connectionId, userCtx);
    case "$disconnect":
      return ConnectionManager.removeConnection(connectionId);
    case "$default":
    default:
      return { statusCode: 404, body: "Invalid Route" };
  }
};

