package main

import (
	"fmt"
	"time"
)

func main() {
	// if
	if a := 100; a == 100 {
		fmt.Println("a == 100")
	} else if a > 10 {
		fmt.Print("a>10")
	} else {
		fmt.Println("a != 100")
	}

	// switch
	b := 50
	switch b {
	case 10, 50:
		fmt.Println("hello")
	case 60, 20:
		fmt.Println("go")
		fallthrough
	case 30:
		fmt.Println("lang")
	default:
		fmt.Println("hehe")
	}

	c := 66
	switch {
	case c > 66:
		fmt.Println("good")
	default:
		fmt.Println("666")
	}

	// for
	for i := 0; i < 10; i++ {
		fmt.Println(i)
	}

	// 死循环
	j := 0
	for {
		if j > 10 {
			break
		}
		time.Sleep(time.Second)
		j++
		fmt.Println(j)
	}

	// range
	str := "abcdef"
	for key, val := range str {
		if key%2 == 0 {
			continue
		}
		fmt.Printf("str[%d] = %c \n", key, val)
	}

	//	for key := range str {
	//		fmt.Printf("str[%d] = %c \n", key, str[key])
	//	}

	// goto
	fmt.Println("start")

	goto end
	fmt.Println("run")
end:
	fmt.Println("end")

}
