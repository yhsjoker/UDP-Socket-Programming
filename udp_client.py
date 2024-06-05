import socket
import time
import config
import argparse
import utils
import numpy as np


def main():
    server_address = get_server_address()
    client_socket = get_client_socket()

    msgs = ["C", "Objective-C", "VB", "C++", "Python", "Java",
            "Rust", "Go", "JavaScript", "C#", "PHP", "ASM"]
    rtt_times = []
    received_pkgs = 0
    start_time = 0
    end_time = 0

    if connect_socket(client_socket, server_address):
        print("Socket connected successfully")
    else:
        print("Socket connected unsuccessfully")
        return

    for seq_no, msg in zip(range(1, len(msgs) + 1), msgs):
        try:
            response, server, rtt = send_msg(client_socket, server_address, seq_no, msg)
            _, _, server_time, rcv_msg = utils.unpack_server_msg(response)

            rtt_times.append(rtt)
            received_pkgs += 1

            if start_time == 0:
                start_time = utils.time_string_to_sec(server_time)
            end_time = max(utils.time_string_to_sec(server_time), end_time)

            print("Received time: {} RPS: {}".format(server_time, rcv_msg))
            print("Received response from {}:{}, Sequence No: {}, RTT: {:.2f} ms".format(server[0], server[1], seq_no, rtt))
        except socket.error:
            print("seq_no {} failed to send".format(seq_no))

    print("Summary:")
    print("Total packets sent: {}".format(len(msgs)))
    print("Total packets received: {}".format(received_pkgs))
    print("Packet loss rate: {:.2f}%".format((1 - received_pkgs / len(msgs)) * 100))
    if rtt_times:
        print("Min RTT: {:.2f} ms".format(min(rtt_times)))
        print("Max RTT: {:.2f} ms".format(max(rtt_times)))
        print("Avg RTT: {:.2f} ms".format(sum(rtt_times) / len(rtt_times)))
        print("Std RTT: {:.2f} ms".format(np.std(rtt_times)))
    print("Total time: {} s".format(end_time - start_time))

    if disconnect_socket(client_socket, server_address):
        print("Socket disconnected successfully")
    else:
        print("Socket disconnected unsuccessfully")


def get_server_address():
    """
    解析命令行参数以获取服务器的IP地址和端口号。
    使用 argparse 库来解析命令行输入的IP地址和端口。

    Returns:
        tuple: 包含服务器的IP地址和端口号。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', default=config.DEFAULT_IP, type=str, help='IP address (default: 127.0.0.1)')
    parser.add_argument('-p', '--port', default=config.DEFAULT_PORT, type=int, help='port number (default: 12345)')
    args = parser.parse_args()
    return args.ip, args.port


def get_client_socket():
    """
    创建并配置一个UDP客户端套接字。

    Returns:
        socket.socket: 配置好的UDP套接字。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(config.TIMEOUT)
    return s


def connect_socket(client_socket, server_address):
    """
    模拟与服务器建立连接。

    Args:
        client_socket (socket.socket): 客户端用于通信的socket对象。
        server_address (tuple): 服务器的地址和端口组成的元组。

    Returns:
        bool: 如果服务器响应为"ok"，则返回True，表示连接成功；否则返回False。
    """
    client_socket.sendto("connect".encode(), server_address)
    response, server = client_socket.recvfrom(1024)
    if response.decode() != "ok":
        return False
    return True


def disconnect_socket(client_socket, server_address):
    """
    模拟尝试与服务器断开连接，并关闭socket。

    Args:
        client_socket (socket.socket): 客户端用于通信的socket对象。
        server_address (tuple): 服务器的地址和端口组成的元组。

    Returns:
        bool: 如果服务器正确响应"disconnect"后，客户端发送确认断开，并关闭socket，返回True；否则返回False。
    """
    client_socket.sendto("disconnect".encode(), server_address)
    response, server = client_socket.recvfrom(1024)
    if response.decode() != "disconnect":
        return False
    client_socket.sendto("disconnected ok".encode(), server_address)
    client_socket.close()
    return True


def send_msg(client_socket, server_address, seq_no, msg):
    """
    向指定的服务器发送一个消息，并等待响应，计算往返时间(RTT)。

    Args:
        client_socket (socket.socket): 客户端套接字。
        server_address (tuple): 服务器的地址和端口。
        seq_no (int): 消息的序列号。
        msg (str): 要发送的消息内容。

    Returns:
        tuple: 包含解码后的响应，服务器地址和RTT毫秒数。

    Raises:
        socket.timeout: 如果在最大重传次数后仍然超时，则抛出超时异常。
    """
    pkg = utils.pack_client_msg(seq_no, config.VERSION, msg)
    print("Sending package {} to {}".format(pkg, server_address))
    start_time = time.time()

    for i in range(config.MAX_RETRIES):
        try:
            client_socket.sendto(pkg.encode(), server_address)
            response, server = client_socket.recvfrom(1024)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000
            return response.decode(), server, rtt
        except socket.timeout:
            if i == 0:
                print("Transmission timed out for packet {}".format(seq_no))
            else:
                print("{}nd retransmission timed out for packet {}".format(i, seq_no))

    raise socket.timeout


if __name__ == "__main__":
    main()
