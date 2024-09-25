f = open('text_file.txt', 'r')
# print(f.read())
f.close()

# or

with open('text_file.txt') as f:
    text = f.read()
    print("file size:", len(text), "characters")
