import socket
import time
import threading
import re


def get_header_body(request_content):
    """获取请求头和body"""

    content = request_content.split(b"\r\n\r\n")

    header = content[0].splitlines()
    body = content[1:]
    res = (header, body)

    return res


def get_post_param(request_body):
    params = request_body[:-1]
    post_dict = {}
    is_boundary = False
    param_byte = b''
    for param in params:
        param_byte += param

    param_str = param_byte.decode()
    if param_str.find('form-data') > -1:
        is_boundary = True

    param_list = param_str.splitlines()
    for param in param_list:
        if param.find('form-data; name') == -1:
            continue
        res = re.split('\"', param)
        if param.find('filename') == -1:
            post_dict[res[1]] = res[2]
        else:
            post_dict[res[1]] = res[3]

    return is_boundary, post_dict


def get_file(request_body):
    return request_body[-1:][0]


def handle_client(client_socket):
    """处理客户端请求"""

    request = client_socket.recv(1024000)
    request_header, request_body = get_header_body(request)
    file_name = "/index.html"

    is_boundary, post_param = get_post_param(request_body)

    if is_boundary:
        with open('11.jpg', 'wb') as f:
            with open('s.log', 'wb') as t:
                t.write(get_file(request_body))
            f.write(get_file(request_body))

    if request_header:
        ret = re.match(r"[^/]+(/[^ ]*)", request_header[0].decode('utf-8'))
        if ret:
            path = ret.group(1)
            if path != '/':
                file_name = path

    if file_name.endswith('.php'):
        fastcgi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fastcgi_socket.connect(('127.0.0.1', 9000))
        fastcgi_socket.send(request)
        r = fastcgi_socket.recv(1024)
        fastcgi_socket.close()
        print(r)
    else:
        try:
            file = open('./html' + file_name, 'rb')
        except Exception as e:
            header = "HTTP/1.1 404 NOT FOUND\r\n"
            header += "content-type: text/html; charset=UTF-8\r\n"
            header += "\r\n"
            content = "404 未找到文件" + file_name
            content = content.encode('utf-8')

            print(e)
        else:
            content_type_map = {
                "css": "text/css",
                "jpg": "image/jpeg",
                "gif": "image/gif",
                "png": "image/png",
                "html": "text/html",
                # "js": "application/javascript",
            }
            content_type = content_type_map["html"]
            file_ext = file_name.split('.')
            if file_ext and file_ext[-1] in content_type_map:
                content_type = content_type_map[file_ext[-1]]
            # 发送数据给客户端
            header = "HTTP/1.1 200 OK\r\n"
            header += "Content-Type: %s; charset=UTF-8\r\n" % content_type
            header += "\r\n"

            # content = "<h1>Hello http server 1.0</h1>"
            # content += "当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            content = file.read()
            file.close()

        client_socket.send(header.encode('utf-8'))
        client_socket.send(content)

    # 关闭链接
    client_socket.close()


def main():
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server_socket.bind(("", 7788))
    tcp_server_socket.listen(128)
    while True:
        client_socket, client_addr = tcp_server_socket.accept()
        worker = threading.Thread(target=handle_client, args=(client_socket,))
        worker.start()
        # handle_client(client_socket)

    tcp_server_socket.close()


if __name__ == "__main__":
    main()
