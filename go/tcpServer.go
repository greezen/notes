package main

import (
	"fmt"
	"net"
	"strings"
)

func main() {
	server, err := net.Listen("tcp", "127.0.0.1:8888")
	if err != nil {
		fmt.Println("err = ", err)
		return
	}
	defer server.Close()

	for {
		conn, err1 := server.Accept()
		if err1 != nil {
			fmt.Println("err1 = ", err1)
			return
		}
		conn.Write([]byte("你好"))

		go HandleMessage(conn)

		fmt.Println(conn.RemoteAddr().String(), " connected")
	}
}

// 接收数据协程
func HandleMessage(conn net.Conn) {
	defer conn.Close()
	for {
		buf := make([]byte, 1024)
		n, err2 := conn.Read(buf)
		if err2 != nil {
			fmt.Println("err2 = ", err2)
			return
		}

		msg := string(buf[:n])
		if msg[:n-2] == "exit" {
			fmt.Println(conn.RemoteAddr().String(), "退出")
			return
		}
		fmt.Print(msg)
		conn.Write([]byte(strings.ToUpper(msg)))
	}
}
