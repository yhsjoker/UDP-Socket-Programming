# UDP Socket Programming

本项目实现了一个基于 UDP 的客户端-服务器消息传输系统，该系统可以模拟数据包丢失，并计算从客户端到服务器发送消息的往返时间（RTT）。

## 功能特点

- **UDP 通信**：使用 UDP 协议实现客户端与服务器之间的消息交换。
- **模拟数据包丢失**：随机模拟数据包丢失，以模拟不可靠的网络条件。
- **计算往返时间**：为每条消息测量并计算往返时间（RTT）。
- **消息重传机制**：实现了在超时情况下消息的重传。

## 系统要求

- Python 3.12
- 必须安装的库详见`requirements.txt`文件

## 项目结构

- `config.py`：包含IP、端口等配置参数。
- `utils.py`：包含消息打包和解包的工具函数。
- `udp_client.py`：实现了UDP客户端，发送消息到服务器并处理响应。
- `udp_server.py`：实现了UDP服务器，接收客户端消息并可选择性地响应。

## 安装步骤

1. **克隆仓库**：
   ```bash
   git clone git@github.com:yhsjoker/UDP-Socket-Programming.git
   cd UDP-Socket-Programming
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 运行应用程序
1. 启动UDP服务器：
   ```bash
   python udp_server.py
   ```
2. 运行UDP客户端：
   ```bash
   python udp_client.py -i <server_ip> -p <server_port>
   ```