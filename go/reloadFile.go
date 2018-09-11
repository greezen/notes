package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"path"
	"time"
)

func main()  {
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

		fileRead.Close()
		fileWrite.Close()
		log.Printf("Copied %d bytes", byteLen)

		err = fileWrite.Sync()
		if err != nil{
			log.Fatal(err)
		} else {
			err := os.Remove(oldfile)
			if err != nil {
				log.Fatal(err)
			}
			os.Rename(newfile, oldfile)
		}

		time.Sleep(2 * time.Second)
	}

	println("转换成功!")
	time.Sleep(time.Second * 5)
}
