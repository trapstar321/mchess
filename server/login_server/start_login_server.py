from server.login_server.message_forwarder import forward_messages
from server.login_server.message_processor import process_messages
from NIO_python.server.NIOServer import Server
import time
from utils.config import load_config
import os

def start_server():
    directory = os.path.dirname(os.path.realpath(__file__))
    file_ = os.path.join(directory, "config.json")
    conf = load_config(file_)["login_server"]
    s = Server(conf, forward_messages, process_messages)
    s.start()

if __name__ == '__main__':
    try:
        conf = load_config("config.json")["login_server"]
        s = Server(conf, forward_messages, process_messages)
        s.start()
    except Exception as ex:
        print(ex)

    while True:
        time.sleep(30)
