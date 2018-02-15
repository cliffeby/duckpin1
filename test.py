f = open("../images/image1.jpg", "rb+")
print(f)
content = f.read()
print("CONTENT LEN", len(content))