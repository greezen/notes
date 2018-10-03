package main

import (
	"fmt"
)

func main() {
	fmt.Println("hello go")
	test()
	test1("bbb")
	test2(1, 2, 3)
	a := test5()
	b, c, d := test6()
	name, age := test7("zs", 15)
	res := calc(15, 6, add)
	fmt.Println(a, b, c, d, name, age, res)

	// 匿名函数
	max, min := func(a, b int) (max, min int) {
		if a > b {
			max = a
			min = b
		} else {
			max = b
			min = a
		}

		return
	}(55, 64)
	fmt.Println(max, min)
}

// 无参无返回值函数
func test() {
	str := "aaa"
	fmt.Println(str)
}

// 有参数无返回值函数
func test1(str string) {
	fmt.Println(str)
}

// 不定参数
func test2(args ...int) {
	fmt.Println(args)
	fmt.Printf("args type is %T\n", args)
	for i, v := range args {
		fmt.Println(i, v)
	}
	// 不定参数传参
	test3(args...)
	test3(args[1:]...)
}

// 不定参数传参
func test3(params ...int) {
	for k, v := range params {
		fmt.Println(k, v)
	}
}

// 无参数有一个返回值
func test4() int {
	return 666
}

func test5() (res int) {
	res = 888
	return
}

// 无参数有多个返回值
func test6() (res int, res1 int, res2 int) {
	res = 11
	res1 = 22
	res2 = 33
	return
}

// 有参数有返回值
func test7(name string, age int, other ...string) (the_name string, the_age int) {
	the_name = name + "t"
	the_age = age + 10
	return
}

// 函数类型和回调函数
func add(a, b int) int {
	return a + b
}

func minus(a, b int) int {
	return a - b
}

type ft func(a, b int) int

func calc(a, b int, f ft) (res int) {
	res = f(a, b)
	return
}
