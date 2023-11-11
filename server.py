import os
import socket
from datetime import datetime
import random
import logging

SERVER_NAME = 'my_server'
IP = '127.0.0.1'
PORT = 25565
QUEUE_LEN = 1
MAX_PACKET = 4
DISCONNECT_MESSEGE = "bye now "

LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/server.log'


def com_name():
    return SERVER_NAME


def com_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def com_rand():
    return str(random.randint(1, 10))


def com_exit(comm_socket):
    # logging.debug("Exiting:")
    comm_socket.close()


def main():
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
                    request = comm.recv(MAX_PACKET).decode()
                    if request == "TIME":
                        time = com_time()
                        comm.send(time.encode())
                        logging.debug(f"sending TIME {time}")
                    if request == "RAND":
                        rnd = com_time()
                        comm.send(rnd.encode())
                        logging.debug(f"sending RAND {rnd}")
                    if request == "NAME":
                        name = com_name()
                        comm.send(com_name().encode())
                        logging.debug(f"sending NAME {name}")
                    if request == "EXIT":
                        ok = False
            except socket.error as err:
                print(err)
                logging.error("error found in the recv phase: " + str(err))
                fine = False
            finally:
                logging.debug(f"EXITING")
                comm.send(DISCONNECT_MESSEGE.encode())
                com_exit(comm)
    except socket.error as err:
        print(err)
        logging.error("error found in binding listening and accepting: " + str(err))
    finally:
        s_socket.close()


if _name_ == '_main_':
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    assert com_name() == SERVER_NAME and 0 < com_rand() < 11 and com_time() == datetime.now().strftime("%H:%M:%S")
    main()