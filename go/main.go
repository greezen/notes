package main

import (
	"calc"
	"fmt"
)

func init() {
	fmt.Println("this is main init")
}

func main() {
	res := calc.Add(1, 2)
	fmt.Println("this is main package!", res)
}
