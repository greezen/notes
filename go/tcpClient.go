package main

import (
	"fmt"
	"io"
	"net"
	"os"
)

var isExit = make(chan bool)

func main() {

	client, err := net.Dial("tcp", "127.0.0.1:8888")
	if err != nil {
		fmt.Println("net.Dial ", err)
		return
	}
	defer client.Close()

	n, err1 := client.Write([]byte("你好，服务器大哥"))
	if err1 != nil {
		fmt.Println("client.Write ", err1)
		return
	}

	if n <= 0 {
		fmt.Println(n, err1)
	}

	// 处理从服务器端接收到的数据
	go HandleMessage(client)

	// 获取用用户输入的内容，并发送到服务端
	go GetMessage(client)

	// 判断用户是否有发送退出的指令
	if <-isExit {
		return
	}
}

// 处理从服务器端接收到的数据
func HandleMessage(conn net.Conn) {
	buf := make([]byte, 1024)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			if err != io.EOF {
				fmt.Println("conn.Read ", err)
			} else {
				isExit <- true
			}
			return
		}
		fmt.Println(string(buf[:n]))
	}
}

// 主动发送数据到服务器端
func SendMessage(conn net.Conn, msg []byte) {
	_, err1 := conn.Write(msg)
	if err1 != nil {
		fmt.Println("conn.Write ", err1)
		return
	}
}

func GetMessage(conn net.Conn) {
	for {
		msg := make([]byte, 1024)
		n, err := os.Stdin.Read(msg)
		if err != nil {
			fmt.Println("os.Stdin.Read ", err)
		}

		// 主动发送数据到服务器端
		go SendMessage(conn, msg[:n])
	}
}
