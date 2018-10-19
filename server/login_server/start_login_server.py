from server.login_server.message_forwarder import forward_messages
from server.login_server.message_processor import process_messages
from NIO_python.server.NIOServer import Server
import time

if __name__ == '__main__':
    try:
        s = Server(10000, 1, False, forward_messages, process_messages)
        s.start()
    except Exception as ex:
        print(ex)

    while True:
        time.sleep(30)
