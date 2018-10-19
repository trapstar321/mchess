from client.login_client.message_forwarder import forward_messages
from client.login_client.message_processor import process_messages
from NIO_python.client.NIOClient import Client


# def create_client(udp_port):
#     c = Client(("localhost", 10000), udp_port, False, forward_messages, process_messages)
#     return c


def create_client(udp_port):
    c = Client(("localhost", 10000), udp_port, False, None, None)
    return c

