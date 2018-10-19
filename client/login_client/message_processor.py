from NIO_python.common.log_optional import Logger
from NIO_python.client.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.client.messages.SM_DISCONNECTED import SM_DISCONNECTED
from client.login_client.messages.SM_CLIENTLIST import SM_CLIENTLIST
from client.login_client.messages.SM_WELCOME import SM_WELCOME
from client.login_client.messages.SM_LOGINFAILED import SM_LOGINFAILED


def process_messages(messages):
    logger = Logger(1)
    try:
        smessages = []
        for message in messages:
            logger.log("Processor received message: {0}".format(message))

            if message["opcode"]==SM_CONNECTED.OP_CODE:
                msg = SM_CONNECTED(message["data"])
                logger.log("Client id={0} connected".format(msg.idx))
            elif message["opcode"]==SM_DISCONNECTED.OP_CODE:
                msg = SM_DISCONNECTED(message["data"])
                logger.log("Client id={0} disconnected".format(msg.idx))
            elif message["opcode"]==SM_CLIENTLIST.OP_CODE:
                msg = SM_CLIENTLIST(message["data"])
                logger.log("Clients on login server={0}".format(msg.clients))
            elif message["opcode"]==SM_LOGINFAILED.OP_CODE:
                msg = SM_LOGINFAILED(message["data"])
                logger.log("Failed to login => {0}".format(msg.msg))
            elif message["opcode"] == SM_WELCOME.OP_CODE:
                msg = SM_WELCOME(message["data"])
                logger.log("Successfull login => {0}".format(msg.msg))
        return smessages
    except Exception as ex:
        logger.log('process_messages exception: {0}'.format(ex))
