from NIO_python.common.log_optional import Logger
from NIO_python.server.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.server.messages.SM_DISCONNECTED import SM_DISCONNECTED
from server.login_server.messages.SM_CLIENTLIST import SM_CLIENTLIST
from server.login_server.messages.CM_LOGIN import CM_LOGIN
from server.login_server.messages.SM_WELCOME import SM_WELCOME
from server.login_server.messages.SM_LOGINFAILED import SM_LOGINFAILED
from server.login_server.messages.SM_LOGGEDIN import SM_LOGGEDIN

users = {}
users['user1'] = {'password': "1234"}
users['user2'] = {'password': "1234"}
users['user3'] = {'password': "1234"}
clients = {}
logger = Logger(1)


def broadcast_message(sender, message, ignore_sender=False):
    try:
        clients_copy = clients.copy()
        if ignore_sender and sender in clients_copy:
            del clients_copy[sender]

        to_send = []

        for client in clients_copy.keys():
            msg = {"id": client, "opcode": message.OP_CODE, "data": message.get_data()}
            to_send.append(msg)

        if len(to_send)>0:
            logger.log("Broadcast message {0}".format(message))

        return to_send
    except Exception as ex:
        logger.log('broadcast_messages exception: {0}'.format(ex))


def client_list(client):
    clients_copy = clients.copy()
    if client in clients_copy.keys():
        del clients_copy[client]

    #remove clients that are not yet logged in
    to_del = []
    for k in clients_copy.keys():
        if 'username' not in clients_copy[k]:
            to_del.append(k)

    for k in to_del:
        del clients_copy[k]

    if len(clients_copy)>0:
        msg = SM_CLIENTLIST(clients_copy)
        msg_data = {"id": client, "opcode": msg.OP_CODE, "data": msg.get_data()}

        logger.log("Send clientlist {0} to client {1}".format(msg, client))
        return msg_data
    else:
        return None


def process_messages(messages, client_id):
    try:
        smessages = []
        for message in messages:
            logger.log("Processor received message: {0}".format(message))

            if message["opcode"] == SM_CONNECTED.OP_CODE:
                clients[message["id"]]={}
            elif message["opcode"] == CM_LOGIN.OP_CODE:
                msg = CM_LOGIN(message["data"])

                if msg.username in users and users[msg.username]["password"] == msg.password:
                    clients[message["id"]] = {"username": msg.username}
                    logger.log("User={0}, login successfull".format(msg.username))
                    ret_msg = SM_WELCOME("Welcome")
                    smessages.append({"id": message["id"], "opcode": ret_msg.OP_CODE, "data": ret_msg.get_data()})

                    # if user logged in successfully broadcast to all clients
                    return_msg = SM_LOGGEDIN(str(message["id"]), msg.username)
                    to_send = broadcast_message(message["id"], return_msg, True)
                    for msg in to_send:
                        smessages.append(msg)
                    cl_list = client_list(message["id"])
                    if cl_list is not None:
                        smessages.append(cl_list)
                else:
                    logger.log("User={0}, login failed".format(msg.username))
                    ret_msg = SM_LOGINFAILED("Incorrect username of password")
                    smessages.append({"id": message["id"], "opcode": ret_msg.OP_CODE, "data": ret_msg.get_data()})

            elif message["opcode"] == SM_DISCONNECTED.OP_CODE:
                del clients[message["id"]]
                return_msg = SM_DISCONNECTED(message["data"])
                to_send = broadcast_message(message["id"], return_msg, True)
                for msg in to_send:
                    smessages.append(msg)

            #logger.log(clients)

        for msg in smessages:
            print("Send message {0}".format(msg))

        return smessages
    except Exception as ex:
        logger.log('process_messages exception: {0}'.format(ex))
