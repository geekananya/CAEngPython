# f = open('text_file.txt', 'r')
# # print(f.read())
# f.close()
#
# # or
# with open('text_file.txt') as f:
#     # print(f.readline())     #first line
#     text = f.read()
#     print(text)
#     print("file size:", len(text), "characters")
#     print("Filename is '{}'.".format(f.name))
#
# f = open('text_file.txt', 'a')
# f.write("Video provides a powerful way to help you prove your point. When you click Online Video, you can paste in the embed code for the video you want to add. You can also type a keyword to search online for the video that best fits your document.")
# f.close()


import csv

# with open('username.csv', 'r') as csvf:
#     csv_reader = csv.reader(csvf)
#     lines =0
#     for row in csv_reader:
#         print(row)
#         lines +=1
#     print("Number of rows =", lines)


with open('employee_birthday.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        # if line_count == 0:
        #     print(f'Column names are {", ".join(row)}')
        #     line_count += 1
        # print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
        # line_count += 1
        print(row)
    print(f'Processed {line_count} lines.')