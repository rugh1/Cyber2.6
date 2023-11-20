"""
Author: Rugh1
Date: 20.11.2023
Description: client  for cyber2.6 work
"""
import logging
import os
import socket

IP = '127.0.0.1'
PORT = 25565
MAX_PACKET = 1024

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/client.log'

COMMANDS = ["EXIT", "NAME", "RAND", "TIME"]
INPUT_MESSAGE = "enter request from EXIT/NAME/RAND/TIME: \n"
SEPERATOR = '!'


def recv(connected_socket):
    """
        receives data using protocol and returns clean string

        :param connected_socket: a socket connected to client
        :returns: string sent from server without extra stuff from protocol
        """
    length = ''
    while True:
        char = connected_socket.recv(1).decode()
        if char == SEPERATOR:
            break
        length += char
    length = int(length)
    return connected_socket.recv(length).decode()




def main():
    """
        main connect sockets and handle everything 
        :returns: None
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((IP, PORT))
        ok = True
        while ok:
            request = input(INPUT_MESSAGE)
            if request in COMMANDS:
                client_socket.send(request.encode())
                answer = recv(client_socket)
                print(answer)
                logging.debug(f"request: {request} and answer {answer}")
                ok = request != "EXIT"
            else:
                print("command doest not exist pls select from EXIT/NAME/RAND/TIME")
    except socket.error as err:
        logging.error(f"error found {err}")
    except Exception as err:
        logging.error(f"error found {err}")
    finally:
        client_socket.close()


if __name__ == '__main__':
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)
    main()
