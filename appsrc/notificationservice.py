import ujson
from libs import logs, queuer, rabbitmq_utils, config, rediscache, sfapi, postgres, utils
LOGGER = logs.LOGGER

SERVICE_NAME='notificationservice'


def treatMessage(dictValue):
    LOGGER.info(dictValue)
    utils.serviceTracesAndNotifies(dictValue, SERVICE_NAME, SERVICE_NAME + ' - Started Processing Notification', False)
    LOGGER.info(" [x] Received id=%r" % (dictValue))
    dictValue['text'] =  'Job - ' + dictValue['jobid']  + ' - ' + dictValue['text']
    # gets the id of the image to retrieve in Redis
    utils.sendNotification(dictValue)
    utils.serviceTracesAndNotifies(dictValue, SERVICE_NAME, SERVICE_NAME + ' - Finished Processing Notification', False)
    LOGGER.info(" [x] Finished id=%r" % (dictValue))

# create a function which is called on incoming messages
def genericCallback(ch, method, properties, body):
    try:
        treatMessage(ujson.loads(body))
    except Exception as e:
        import traceback
        traceback.print_exc()
        LOGGER.error(e.__str__())

if __name__ == "__main__":
    queuer.initQueuer()
    queuer.listenToTopic(config.SUBSCRIBE_CHANNEL, 
    {
        config.QUEUING_KAFKA : treatMessage,
        config.QUEUING_CLOUDAMQP : genericCallback,
    })

