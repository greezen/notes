import socket

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(("", 7777))
    while True:
        msg = s.recvfrom(1024)
        print(msg[1], ':', msg[0].decode('utf-8'))


if __name__ == "__main__":
    main()
