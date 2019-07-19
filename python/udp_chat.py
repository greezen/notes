import socket

def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #udp_socket.bind(("", 7778))
    ip = input("请输入IP:")
    port = int(input("请输入端口:"))
    msg = input("请输入内容:").encode("utf-8")

    udp_socket.sendto(msg, (ip, port))

    rsp = udp_socket.recvfrom(1024)
    print(rsp)

if __name__ == "__main__":
    main()
