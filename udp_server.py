import socket
import random

import config
import utils


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((config.DEFAULT_IP, config.DEFAULT_PORT))
    print(f"Server listening on {config.DEFAULT_IP}:{config.DEFAULT_PORT}")

    while True:
        pkg, address = server_socket.recvfrom(config.SEQ_LENGTH + config.VERSION_LENGTH + config.MAX_MSG_LENGTH)
        if random.random() >= config.LOSS_RATE:
            sequence_number, version, msg = utils.unpack_client_msg(pkg.decode())
            pkg = utils.pack_server_msg(sequence_number, version, msg + " language")

            print("Send package {}".format(pkg))
            server_socket.sendto(pkg.encode(), address)
        else:
            print(f"Simulated packet loss for request from {address}")


if __name__ == "__main__":
    main()
