import threading


def test1():
    print("this is test1")


def test2():
    print("this is test2")

def main():
    t1 = threading.Thread(target=test1)
    t2 = threading.Thread(target=test2)
    
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()
