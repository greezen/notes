//按照指定文件顺序来修改mp3的创建时间
package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"strconv"
	"strings"
	"time"
)

// 单位换算
const (
	BYTE = 1 << (10 * iota)
	KILOBYTE
	MEGABYTE
	GIGABYTE
	TERABYTE
)

func main()  {
	println("处理中...")
	dir := "./"
	files, _ := ioutil.ReadDir(dir)
	i := 0
	for _, fi := range files {
		if path.Ext(fi.Name()) != ".mp3" {
			continue
		}

		i++
		fileRead, err := os.Open(fi.Name())
		if err != nil {
			log.Fatal(err)
		}

		oldfile := fi.Name()
		newfile := fmt.Sprintf("%s%d%s", "b", i, fi.Name())
		fileWrite, err := os.Create(newfile)
		if err != nil {
			log.Fatal(err)
		}

		byteLen, err := io.Copy(fileWrite, fileRead)
		if err != nil {
			log.Fatal(err)
		}

		log.Printf("Copied %s", HumanSize(byteLen))

		err = fileWrite.Sync()
		fileRead.Close()
		fileWrite.Close()
		if err != nil{
			log.Fatal(err)
		} else {
			err := os.Remove(oldfile)
			if err != nil {
				log.Fatal(err)
			}
			err = os.Rename(newfile, oldfile)
		}

		time.Sleep(2 * time.Second)
	}

	println("转换完成!")
	time.Sleep(2 * time.Second)
}

// 格式化字节
func HumanSize(bytes int64) string {
	unit := ""
	value := float64(bytes)

	switch {
	case bytes >= TERABYTE:
		unit = "T"
		value = value / TERABYTE
	case bytes >= GIGABYTE:
		unit = "G"
		value = value / GIGABYTE
	case bytes >= MEGABYTE:
		unit = "M"
		value = value / MEGABYTE
	case bytes >= KILOBYTE:
		unit = "K"
		value = value / KILOBYTE
	case bytes >= BYTE:
		unit = "B"
	case bytes == 0:
		return "0"
	}

	result := strconv.FormatFloat(value, 'f', 1, 64)
	result = strings.TrimSuffix(result, ".0")
	return result + unit
}
