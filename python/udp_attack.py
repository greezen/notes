import socket
import random
import string


def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest_ip = input("目标ip:")
    dest_port = int(input("目标port:"))
    dest = (dest_ip, dest_port)
    while(True):
        msg = ''.join(random.choices(string.ascii_letters + string.digits, k=512))
        res = udp_socket.sendto(msg.encode("utf-8"), dest)
        print(res)

    udp_socket.close()

if __name__ == "__main__":
    main()
