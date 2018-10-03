package main

import (
	"fmt"
	"os"
)

func t(x int) {
	res := 100 / x
	fmt.Println(res)
}

func t1() {
	a := 5
	b := 9
	defer func(a, b int) {
		fmt.Println(a, b)
	}(a, b)

	a = 11
	b = 34

	fmt.Println(a, b)
}

func main() {
	t1()
	// main函数执行完后，defer函数先进后出,有错误也会执行哦
	defer fmt.Println("first")
	defer fmt.Println("second")
	defer t(0)
	defer fmt.Println("third")
	fmt.Println(os.Args)

}
