import os

try:
    import pysubs2
except ImportError:
    if os.name.startswith('win'):
        os.system('python -m pip install pysubs2')
    else:
        os.system('python3 -m pip install pysubs2')
    try:
        import pysubs2
    except ImportError:
        print("You don't have python installed!")
        exit()


while True:
    option = input('E/xtrcat text | M/odify text >> ').lower()
    if option != '' and option == 'e':
        file = input("Name of the subs (ex: test.ass) >> ")
        if file != '':
            savefile = input("Name of the modified subs (ex: test.txt) >> ")
            if savefile != '':
                break
    elif option != '' and option == 'm':
        file = input('Input file (ex: subs.ass) >> ')
        if file != '':
            savefile = input('Modified text (ex: text.txt) >> ')
            if savefile != '':
                break


if option == 'e':
    subs = pysubs2.load(file, encoding="utf-8")
    textFile = open(savefile, 'a')
    for line in subs:
        print(line.text)
        textFile.write(line.text+'\n')
    textFile.close()
    print('Extracted all text')
else:
    subs = pysubs2.load(file, encoding="utf-8")
    lines = []
    fileMod = open(savefile, 'rt')
    for l in fileMod:
        if '\n' in l:
            l = l.replace('\n', '')
        lines.append(l)
    ind = 0
    for line in subs:
        line.text = lines[ind]
        ind += 1
    subs.save(file)
    print('Saved')

