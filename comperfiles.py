while True:
    name = input("Enter the name of the file (example: text.txt | D:/folder_nme/filename.txt) >> ")
    name2 = input("Enter the name of the second file (example: text.txt | D:/folder_nme/filename.txt) >> ")
    ty = input("Are the files text? Y/N >> ")
    ty = ty.lower()
    if name2 != "" and name != "" and ty != "":
        break
    if name == name2:
        print("The names of the files are equal")

try:
    if ty == "yes" or ty == "y":
        file = open(name, "rt")
        file2 = open(name2, "rt")
    else:
        file = open(name, "rb")
        file2 = open(name2, "rb")
except Exception:
    print("Check if the file exists and check if the file is in the right format. An exception was raised.")
    exit()


lines = []
lines2 = []


for line in file:
    if "\n" in line:
        line = line.replace("\n", "")
    lines.append(line)

for line4 in file2:
    if "\n" in line4:
        line4 = line4.replace("\n", "")
    lines2.append(line4)


print("")
file1Size = len(lines)
file2Size = len(lines2)

if file1Size != file2Size or lines != lines2:
    print("!< - > Different < - >!")
    if file1Size != file2Size:

        print(name + " have " + str(file1Size) + " lines")
        print(name2 + " have " + str(file2Size) + " lines")
    print("")
    if lines != lines2:
        justLines = []

        for lineInFile in lines:
            if lineInFile not in lines2:
                justLines.append(lineInFile)
                print(name + " -> " + lineInFile + " is not in " + name2)
        for lineInFile2 in lines2:
            if lineInFile2 not in lines and lineInFile2 not in justLines:
                print(name2 + " -> " + lineInFile2 + " is not in " + name)


else:
    print("< + > Equal < + > :)")
