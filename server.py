"""
Author: Rugh1
Date: 20.11.2023
Description: server  for cyber2.6 workt
"""
import os
import socket
from datetime import datetime
import random
import logging
import sys

thismodule = sys.modules[__name__]

SEPERATOR = '!'
SERVER_NAME = 'my_server'
IP = '127.0.0.1'
PORT = 25565
QUEUE_LEN = 1
MAX_PACKET = 4
DISCONNECT_MESSAGE = "bye now "

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def send(connected_socket, msg):
    """
    send to client using protocol

    :param connected_socket: a socket connected to client
    :param msg: this is a second param
    :returns: None
    """
    msg = str(len(msg)) + SEPERATOR + msg
    connected_socket.send(msg.encode())


def com_name():
    """
        returns server name

        :returns: server name
        :rtype: string
    """
    return SERVER_NAME


def com_time():
    """
        returns current time in %H:%M:%S format

        :returns: current time in %H:%M:%S format
        :rtype: string
    """
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def com_rand():
    """
        returns random int between 1 and 10

        :returns:  random int between 1 and 10
        :rtype: string
    """
    return str(random.randint(1, 10))


def com_exit(comm_socket):
    """
        closing socket

        :returns: None
     """
    comm_socket.close()


def main():
    """
        main connect sockets and handle everything 
        :returns: None
    """
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_socket.bind((IP, PORT))
        s_socket.listen(QUEUE_LEN)
        fine = True
        while fine:
            print("connecting...")
            comm, addr = s_socket.accept()
            print(f"connected with: {addr}")
            try:
                ok = True
                while ok:
                    request = comm.recv(MAX_PACKET).decode().replace(' ', '').lower()
                    if request != 'exit':
                        # hi nir here is a nice comment im shocked this type of thing is possible and so simple
                        # im literally shaking 😲
                        func = getattr(thismodule, f'com_{request}')
                        data_to_send = func()
                        logging.debug(f"requested: {request} sending {data_to_send}")
                        send(comm, data_to_send)
                    else:
                        ok = False
            except socket.error as err:
                print(err)
                logging.error("error found in the recv phase: " + str(err))
                ok = False
            except Exception as err:
                print(err)
                logging.error(str(err))
                ok = False
            finally:
                logging.debug(f"closing connection with client")
                try:
                    send(comm, DISCONNECT_MESSAGE)
                except socket.error as err:
                    logging.error("client probbly crashed good bye msg couldnt send" + str(err))
                com_exit(comm)
    except socket.error as err:
        print(err)
        logging.error("error found in binding listening and accepting: " + str(err))
    finally:
        s_socket.close()


if __name__ == '__main__':
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    assert com_name() == SERVER_NAME and 0 < int(com_rand()) < 11 and com_time() == datetime.now().strftime("%H:%M:%S")
    main()
