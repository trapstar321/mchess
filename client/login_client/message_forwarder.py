import queue

from NIO_python.common.log_optional import Logger

import datetime
import socket

s = None
e = None


def forward_messages(udp_port, read_queue, write_queue, process_messages, debug, pings):
    global s
    global e

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

                processed_messages = process_messages(messages)

                if len(processed_messages)>0:
                    write_queue.put(processed_messages)

                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    sock.sendto(b'1', ('127.0.0.1', udp_port))

                if s:
                    e = datetime.datetime.now()
                    pings.put((e - s).microseconds / 1000)
            except Exception as ex:
                logger.log("forward_messages: exception: {0}".format(ex))
            s = datetime.datetime.now()
