import socket


def handle_client(client_socket):
    """
    处理客户端消息
    """
    # 有新的客户端请求
    while True:
        # 接收数据
        msg = client_socket.recv(1024)
        # 客户端断开链接或没有消息时退出服务
        if not msg:
            break

        print(msg.decode('utf-8').strip("\n"))

        send_msg = input("请输入发送内容：") + "\n"
        # 发送数据
        client_socket.send(send_msg.encode('utf-8'))

    # 关闭客户端socket
    client_socket.close()

def main():
    # 创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定端口
    addr = ("", 9999)
    tcp_socket.bind(addr)

    # 监听 最大128个链接
    tcp_socket.listen(128)

    # 阻塞接收请求
    client_socket, client_addr = tcp_socket.accept()
    print(client_addr)

    handle_client(client_socket)

    # 关闭服务端socket
    tcp_socket.close()


if __name__ == "__main__":
    main()
