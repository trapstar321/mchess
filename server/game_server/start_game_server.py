from server.game_server.message_forwarder import forward_messages
from server.game_server.message_processor import process_messages
from NIO_python.server.NIOServer import Server
import time
from utils.config import load_config

if __name__ == '__main__':
    try:
        conf = load_config("config.json")
        s = Server(conf, forward_messages, process_messages)
        s.start()
    except Exception as ex:
        print(ex)

    while True:
        time.sleep(30)
