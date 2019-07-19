import socket


def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    addr = ("192.168.2.102", 1234)
    tcp_socket.connect(addr)

    msg = input("请输入内容：")
    tcp_socket.send(msg.encode('utf-8'))

    tcp_socket.close()

if __name__ == "__main__":
    main()
