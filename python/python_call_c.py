from ctypes import *
import threading

def main():
    lib = cdll.LoadLibrary("./output.so")
    #t = threading.Thread(target=lib.loop, args=('python'))
    msg = input("请输入要打印的内容：")
    lib.output(msg.encode("utf-8"))

if __name__ == "__main__":
    main()
