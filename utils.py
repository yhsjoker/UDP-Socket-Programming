import time

import config


def pack_client_msg(seq_no: int, ver: int, msg: str):
    """
    将客户端的消息打包成特定格式。

    Args:
        seq_no (int): 消息的序列号。
        ver (int): 使用的协议版本号。
        msg (str): 要发送的消息内容。

    Returns:
        str: 格式化后的消息字符串。

    Raises:
        ValueError: 如果输入的序列号或版本号不在规定范围内，或消息长度超过最大限制。
    """
    if seq_no < config.MIN_SEQ_NO or seq_no > config.MAX_SEQ_NO:
        raise ValueError("Sequence number out of range")
    if ver is not config.VERSION:
        raise ValueError("Version number error")
    if len(msg) > config.MAX_MSG_LENGTH:
        raise ValueError("Message too long")
    return "{:0>2d}{}{}".format(seq_no, ver, msg.ljust(config.MAX_MSG_LENGTH, '*'))


def unpack_client_msg(msg: str):
    """
    从接收到的客户端消息中解包数据。

    Args:
        msg (str): 接收到的完整消息字符串。

    Returns:
        tuple: 包含序列号，版本号和消息内容的元组。

    Raises:
        ValueError: 如果消息的格式不正确。
    """
    if len(msg) is not config.SEQ_LENGTH + config.VERSION_LENGTH + config.MAX_MSG_LENGTH:
        raise ValueError("Message error")
    return (int(msg[:config.SEQ_LENGTH]), int(msg[config.SEQ_LENGTH:config.SEQ_LENGTH + config.VERSION_LENGTH]),
            msg[config.SEQ_LENGTH + config.VERSION_LENGTH:].rstrip('*'))


def pack_server_msg(seq_no: int, ver: int, msg: str):
    """
    将服务器的消息和当前时间戳打包成特定格式发送给客户端。

    Args:
        seq_no (int): 消息的序列号。
        ver (int): 使用的协议版本号。
        msg (str): 要发送的消息内容。

    Returns:
        str: 格式化后包含时间戳的消息字符串。

    Raises:
        ValueError: 如果序列号或版本号不在规定范围内，或消息加上时间戳后的长度超过了最大限制。
    """
    if seq_no < config.MIN_SEQ_NO or seq_no > config.MAX_SEQ_NO:
        raise ValueError("Sequence number out of range")
    if ver is not config.VERSION:
        raise ValueError("Version number error")
    if len(msg) + 8 > config.MAX_MSG_LENGTH:
        raise ValueError("Message too long")
    return "{:0>2d}{}{}{}".format(seq_no, ver, time.strftime("%H-%M-%S", time.localtime()),
                                  msg.ljust(config.MAX_MSG_LENGTH - 8, '*'))


def unpack_server_msg(msg: str):
    """
    从接收到的服务器消息中解包数据和时间戳。

    Args:
        msg (str): 接收到的完整消息字符串。

    Returns:
        tuple: 包含序列号，版本号，时间戳和消息内容的元组。

    Raises:
        ValueError: 如果消息的格式不正确。
    """
    if len(msg) is not config.SEQ_LENGTH + config.VERSION_LENGTH + config.MAX_MSG_LENGTH:
        raise ValueError("Message error")
    return (int(msg[:config.SEQ_LENGTH]), int(msg[config.SEQ_LENGTH:config.SEQ_LENGTH + config.VERSION_LENGTH]),
            msg[config.SEQ_LENGTH + config.VERSION_LENGTH: config.SEQ_LENGTH + config.VERSION_LENGTH + 8],
            msg[config.SEQ_LENGTH + config.VERSION_LENGTH + 8:].rstrip('*'))


def time_string_to_sec(time_str):
    """
    将时间字符串转换为从午夜开始的秒数。

    Args:
        time_str (str): 格式为 "HH-MM-SS" 的时间字符串。

    Returns:
        int: 从午夜开始计算的秒数。
    """
    ts = time_str.split('-')
    return int(ts[0]) * 3600 + int(ts[1]) * 60 + int(ts[2])