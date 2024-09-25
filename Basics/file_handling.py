f = open('text_file.txt', 'r')
# print(f.read())
f.close()

# or

with open('text_file.txt') as f:
    print(f.readline())     #first line
    text = f.read()
    print("file size:", len(text), "characters")
    print("Filename is '{}'.".format(f.name))
