import socket
import struct
from ctypes import *


class IP(Structure):
    _fields_ = [
                ("ihl", c_ubyte, 4),
                ("version", c_ubyte, 4),
                ("tos", c_ubyte),
                ("len", c_ushort),
                ("id", c_ushort),
                ("offset", c_ushort),
                ("ttl", c_ubyte),
                ("protocol_num", c_ubyte),
                ("sum", c_ushort),
                ("src", c_ulong),
                ("dst", c_ulong)
            ]
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        print(self.src, struct.pack('<L', self.src))
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)




