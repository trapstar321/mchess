from NIO_python.server.message_forwarder import forward_messages
from NIO_python.server.message_processor import process_messages
from NIO_python.server.NIOServer import Server

if __name__=="__main__":
    import time

    try:
        s = Server(10000, 1, True, forward_messages, process_messages)
        s.start()
    except Exception as ex:
        print(ex)

    time.sleep(600)