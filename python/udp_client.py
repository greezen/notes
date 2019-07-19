import socket

def main():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            msg = input("请输入:\n") + "\n" 
            udp_socket.sendto(msg.encode("utf-8"), ("192.168.8.36", 6666))
    except:
        print("出错了")
    finally:
        udp_socket.close()

if __name__ == "__main__":
    main()
