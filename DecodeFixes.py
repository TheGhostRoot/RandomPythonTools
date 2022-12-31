# Translator Decode fix:

"""
def writeToFile(file, text):
    f = open(file, 'a', encoding='utf-8')
    f.write(text)
    f.write('\n')
    f.close()
"""

# ManageSubs Decode fix:

"""
import pysubs2

def Subs(option, file, savefile):
    if option == 'e':
        subs = pysubs2.load(file, encoding="utf-8", errors='ignore')
        textFile = open(savefile, 'a', encoding="utf-8")
        for line in subs:
            print(line.text)
            textFile.write(line.text+'\n')
        textFile.close()
        print('Extracted all text')
    else:
        subs = pysubs2.load(file, encoding="utf-8", errors='ignore')
        lines = []
        fileMod = open(savefile, encoding="utf-8")
        for l in fileMod:
            if '\n' in l:
                l = l.replace('\n', '')
            lines.append(l)
        ind = 0
        for line in subs:
            line.text = lines[ind]
            ind += 1
        subs.save(file)
        print('Saved modified version')

"""