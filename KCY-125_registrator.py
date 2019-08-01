import hashlib


string = input("enter the string: ")
hashlib.md5()
first = hashlib.md5(string.encode('utf-8')).hexdigest()
second = hashlib.md5(first.encode('utf-8')).hexdigest()
print("md5 hash is:\n\r" + first + "\n\r" + second)
