package main

import "fmt"

func main() {
	// 1.bool
	var bl bool
	bl = true
	fmt.Println("bl = ", bl)

	// 2. int
	var i int
	i = 33
	fmt.Println("i = ", i)

	// 3. float
	var f float32
	f = 5.66

	f1 := 3.55
	fmt.Printf("f=%f,f1=%f,f type is %T, f1 type is %T", f, f1, f, f1)
	fmt.Println()

	// 4. byte
	var bt, ch byte
	bt = 97
	ch = 'a'
	fmt.Printf("bt = %c, ch= %d", bt, ch)
	fmt.Println()

	// 5. string
	var str string
	str1 := "我是字符串"
	str = "asdf"
	fmt.Println(str, str1, len(str1), len(str))
	fmt.Printf("str[1]=%c\n", str[1])

	// 6. complex
	var t complex128
	t = 2.1 + 3.14i
	t2 := 5.1 + 5.14i
	fmt.Println(t, t2)
	fmt.Println(real(t), imag(t))

	// format
	fm1 := 10
	fm2 := "aaa"
	fm3 := 'D'
	fm4 := 3.1415926

	// 变量类型
	fmt.Printf("%T %T %T %T \n", fm1, fm2, fm3, fm4)
	// 有同类型的变量值
	fmt.Printf("%d %s %c %f \n", fm1, fm2, fm3, fm4)
	// 自动判断变量
	fmt.Printf("%v %v %v %v \n", fm1, fm2, fm3, fm4)

	// input
	var v int
	fmt.Println("please input a value:")
	fmt.Scanf("%d", &v)
	fmt.Println("v=", v)

	// 类型别名
	type (
		long int64
		char byte
	)
	type bigint int64
	var tb bigint = 10
	var tl long = 55
	var tc char = 65
	fmt.Println(tb)
	fmt.Printf("tb type is %T, tl type is %T, tc type is %T", tb, tl, tc)

}
