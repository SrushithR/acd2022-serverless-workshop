exports.publishMessage = async (event, _context, callback) => {
    const {
      userContext,
      body: { message }
    } = event;
    console.log("Event ", JSON.stringify(event));
  
    if (
      !message.messageType ||
      !message.eventType ||
      !userContext ||
      !message.data
    ) {
      console.error("Missing required fields");
      return callback(new PublishValidationError("Missing required fields"));
    }
  
    const gwEndpoint = `https://${WEBSOCKET_DOMAIN}/${STAGE}`;
    return publishMessageHelper(userContext, message, gwEndpoint)
      .then(successCount => {
        console.log("Message published successfully to clients");
        callback(null, {
          statusCode: 200,
          body: `Message successfully published to ${successCount} connections`
        });
      })
      .catch(err => {
        console.error("Failed to publish message");
        callback(err);
      });
  };
  