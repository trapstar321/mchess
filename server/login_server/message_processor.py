from NIO_python.common.log_optional import Logger
from NIO_python.server.messages.SM_CONNECTED import SM_CONNECTED
from NIO_python.server.messages.SM_DISCONNECTED import SM_DISCONNECTED
from server.login_server.messages.SM_CLIENTLIST import SM_CLIENTLIST
from server.login_server.messages.CM_LOGIN import CM_LOGIN
from server.login_server.messages.SM_WELCOME import SM_WELCOME
from server.login_server.messages.SM_LOGINFAILED import SM_LOGINFAILED
from server.login_server.messages.SM_LOGGEDIN import SM_LOGGEDIN
from server.login_server.messages.CM_GAMEREQUEST import CM_GAMEREQUEST
from server.login_server.messages.SM_GAMEREQUEST import SM_GAMEREQUEST
from server.login_server.messages.SM_GAMEREQUESTERROR import SM_GAMEREQUESTERROR
from server.login_server.messages.CM_ACCEPTGAMEREQUEST import CM_ACCEPTGAMEREQUEST
from server.login_server.messages.CM_REJECTGAMEREQUEST import CM_REJECTGAMEREQUEST
from server.login_server.messages.CM_CANCELGAMEREQUEST import CM_CANCELGAMEREQUEST
from server.login_server.messages.SM_CANCELGAMEREQUEST import SM_CANCELGAMEREQUEST
from server.login_server.messages.SM_REJECTGAMEREQUEST import SM_REJECTGAMEREQUEST
from server.login_server.messages.SM_GAMEKEY import SM_GAMEKEY
import uuid
import json
from utils.aes import encrypt, to_hex

from models.server.gamerequest import GameRequest

users = {}
users['user1'] = {'password': "1234"}
users['user2'] = {'password': "1234"}
users['user3'] = {'password': "1234"}
users['user4'] = {'password': "1234"}
clients = {}
logger = Logger(1)

requests = []


def broadcast_message(sender, message, ignore_sender=False):
    try:
        clients_copy = clients.copy()
        if ignore_sender and sender in clients_copy:
            del clients_copy[sender]

        to_send = []

        for client in clients_copy.keys():
            #broadcast only to logged in users
            if 'username' in clients_copy[client]:
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

def game_request_control(from_, to):
    for request in requests:
        if request.to == to and request.from_ == from_:
            logger.log("Request control returned error \"{0}\"".format("Request to user was already sent"))
            return SM_GAMEREQUESTERROR("Request to user was already sent")
    return None

def cancel_game_request_control(request_id, from_):
    for request in requests:
        if request.request_id==request_id and request.from_ == from_:
            return True
    return False

def reject_game_request_control(request_id, to):
    for request in requests:
        if request.request_id==request_id and request.to == to:
            return True
    return False

def delete_requests(client_id):
    global requests
    new_list = []

    for request in requests:
        if request.from_ == client_id or request.to == client_id:
            pass
        else:
            new_list.append(request)

    requests = new_list

def delete_request(request_id):
    global requests
    new_list = []

    for request in requests:
        if request.request_id == request_id:
            pass
        else:
            new_list.append(request)

    requests = new_list


def get_gamerequest_destination(request_id):
    for request in requests:
        if request.request_id==request_id:
            return request.to

    return None

def get_gamerequest_source(request_id):
    for request in requests:
        if request.request_id==request_id:
            return request.from_

    return None

def process_messages(messages, conf, client_id):
    global requests

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
                    return_msg = SM_LOGGEDIN(message["id"], msg.username)
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

                delete_requests(message["id"])
            elif message["opcode"] == CM_GAMEREQUEST.OP_CODE:
                msg = CM_GAMEREQUEST(message["data"])

                error = game_request_control(message["id"], msg.client)
                if error:
                    smessages.append({"id": message["id"], "opcode": error.OP_CODE, "data": error.get_data()})
                else:
                    logger.log("Game request to {0} from {1}".format(msg.client, message["id"]))
                    request_id = uuid.uuid1()

                    src_name = clients[message["id"]]["username"]
                    dest_name = clients[msg.client]["username"]

                    destination_msg = SM_GAMEREQUEST(request_id, message["id"], src_name, 0)
                    source_msg = SM_GAMEREQUEST(request_id, msg.client, dest_name, 1)

                    smessages.append({"id": msg.client, "opcode": destination_msg.OP_CODE, "data": destination_msg.get_data()})
                    smessages.append({"id": message["id"], "opcode": source_msg.OP_CODE, "data": source_msg.get_data()})

                    gr = GameRequest(request_id, message["id"], msg.client)
                    requests.append(gr)
            elif message["opcode"] == CM_CANCELGAMEREQUEST.OP_CODE:
                msg = CM_CANCELGAMEREQUEST(message["data"])
                request_id = msg.request_id
                if cancel_game_request_control(request_id, message["id"]):
                    logger.log('Cancel request {0}'.format(request_id))
                    msg = SM_CANCELGAMEREQUEST(request_id)
                    smessages.append({"id": message["id"], "opcode": msg.OP_CODE, "data": msg.get_data()})
                    smessages.append({"id": get_gamerequest_destination(request_id), "opcode": msg.OP_CODE, "data": msg.get_data()})
                    delete_request(request_id)
                else:
                    logger.log('Cancel request {0} failed'.format(request_id))
                    msg = SM_GAMEREQUESTERROR('Cancel request failed')
                    smessages.append({"id": message["id"], "opcode": msg.OP_CODE, "data": msg.get_data()})
            elif message["opcode"] == CM_REJECTGAMEREQUEST.OP_CODE:
                msg = CM_REJECTGAMEREQUEST(message["data"])
                request_id = msg.request_id
                if reject_game_request_control(request_id, message["id"]):
                    logger.log('Reject request {0}'.format(request_id))
                    msg = SM_REJECTGAMEREQUEST(request_id)
                    smessages.append({"id": message["id"], "opcode": msg.OP_CODE, "data": msg.get_data()})
                    smessages.append({"id": get_gamerequest_source(request_id), "opcode": msg.OP_CODE, "data": msg.get_data()})
                    delete_request(request_id)
                else:
                    logger.log('Reject request {0} failed'.format(request_id))
                    msg = SM_GAMEREQUESTERROR('Reject request failed')
                    smessages.append({"id": message["id"], "opcode": msg.OP_CODE, "data": msg.get_data()})
            elif message["opcode"] == CM_ACCEPTGAMEREQUEST.OP_CODE:
                msg = CM_ACCEPTGAMEREQUEST(message["data"])
                request_id = msg.request_id

                dest = get_gamerequest_destination(request_id)
                src = get_gamerequest_source(request_id)
                dest_username = clients[dest]["username"]
                src_username = clients[src]["username"]

                key = {"user1": dest_username, "user2": src_username}
                key = to_hex(encrypt(conf["aes_key"], json.dumps(key)))

                game_server = conf["game_servers"][0]
                ip = game_server["ip"]
                port = game_server["port"]

                msg = SM_GAMEKEY(ip, port, key)
                smessages.append({"id": dest, "opcode": msg.OP_CODE, "data": msg.get_data()})
                smessages.append({"id": src, "opcode": msg.OP_CODE, "data": msg.get_data()})

            #logger.log(clients)

        for msg in smessages:
            logger.log("Send message {0}".format(msg))

        return smessages
    except Exception as ex:
        logger.log('process_messages exception: {0}'.format(ex))
