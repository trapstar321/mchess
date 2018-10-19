import queue
import socket
from NIO_python.common.log_optional import Logger


def forward_messages(udp_port, read_queue, write_queue, process_messages, debug):
    logger = Logger(debug)
    while True:
        try:
            messages = read_queue.get()
        except queue.Empty:
            pass
        else:
            try:
                if len(messages) == 1 and messages[0] == {}:
                    logger.log('Exit forwarder')
                    return

                processed_messages = process_messages(messages, None)

                if len(messages)>0:
                    write_queue.put(processed_messages)

                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(b'1', ('127.0.0.1', udp_port))

            except Exception as ex:
                print('forward_messages: exception: {0}'.format(ex))

