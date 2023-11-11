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
INPUT_MESSAGE = "enter request from EXIT/NAME/RAND/TIME"

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((IP, PORT))
        ok = True
        while ok:
            request = input(INPUT_MESSAGE)
            if request in COMMANDS:
                client_socket.send(request.encode())
                answer = client_socket.recv(MAX_PACKET).decode()
                print(answer)
                logging.debug(f"request: {request} and answer {answer}")
                ok = request != "EXIT"
            else:
                print("command doest not exist pls select from EXIT/NAME/RAND/TIME")
    except socket.error as err:
        logging.error(f"error found {err}")


if __name__ == '_main_':
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    main()