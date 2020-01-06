import socket
import os
from sniffer_ip_header_decode import IP


def main():
    host = "127.0.0.1"
    if os.name == "nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    sniffer.bind((host, 0))

    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name  == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = sniffer.recvfrom(65565)
            print(raw_buffer)
            ip_header = IP(raw_buffer[0][0:100])
            print("Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))
    except Exception as rt:
        print(rt)
        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == "__main__":
    main()
