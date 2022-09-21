while True:
    fileName = input("Enter the name of the file (example: text.txt) >> ")
    if fileName != "":
        break

file = open(fileName, "rt")
lines = []

for line in file:
    if line in lines:
        print("Duplicated > "+line)
    else:
        lines.append(line)
