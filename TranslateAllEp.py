import os

try:
    from google_translate_py import Translator
    import deep_translator as deep
    import dl_translate as dlt
    import langdetect
    import pysubs2
except ImportError:
    if os.name.startswith('win'):
        os.system("python -m pip install google-translate.py deep_translator dl-translate langdetect pysubs2")
    else:
        os.system("python3 -m pip install google-translate.py deep_translator dl-translate langdetect pysubs2")
    try:
        from google_translate_py import Translator
        import deep_translator as deep
        import dl_translate as dlt
        import langdetect
        import pysubs2
    except ImportError:
        print("Try installing google-translate.py deep_translator dl-translate langdetect pysubs2 with python3.7+")
        exit()


languages = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh': 'chinese',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}


def allLangs():
    print(str(len(languages)) + " languages available")
    print("")
    n = 0
    for lang in languages.values():
        n += 1
        print(str(n) + " -> " + lang)


def writeToFile(file, text):
    f = open(file, 'a', encoding='utf-8')
    f.write(text)
    f.write('\n')
    f.close()


def getLang(langInd: int):
    KEYS = []
    for key in languages:
        KEYS.append(key)
    return KEYS[langInd]


def trans(fileName: str, saveName: str, translateToAllLangs: bool, langInd: int):
        file = open(fileName, "rt")
        langKey = getLang(langInd)
        if not (translateToAllLangs):
            open(saveName, "a")
        translator2 = deep.GoogleTranslator(source='auto', target=langKey)
        mt = dlt.TranslationModel()
        translator = Translator()
        # the file is NOT CONFIG
        lines = []
        for line in file:
            if "\n" in line:
                line = line.replace("\n", "")
            lines.append(line)
        if translateToAllLangs:
            for key in languages.keys():
                newName = ""
                for char in saveName:
                    if char == ".":
                        break
                    else:
                        newName += char
                fileType = ""
                done = False
                for char in saveName:
                    if char == "." or done:
                        fileType += char
                        done = True
                #saveFile = open(newName + "-" + key + fileType, "a")
                saveName1 = newName + "-" + key + fileType
                for l in lines:
                    if l != "":
                        try:
                            t = l if l.isdigit() or l.isdecimal() else translator.translate(l, "", key)
                        except Exception:
                            try:
                                translator2 = deep.GoogleTranslator(source="auto", target=key)
                                t = l if l.isdigit() or l.isdecimal() else translator2.translate(text=l)
                            except Exception:
                                t = l if l.isdigit() or l.isdecimal() else mt.translate(l, source=languages.get(langdetect.detect(l)).capitalize(), target=languages.get(key).capitalize())
                        if "„" in t:
                            t = t.replace("„", '"')
                        writeToFile(saveName1, t+'\n')
                        #saveFile.write(t + "\n")
                        print(l + " -> " + t)
                    else:
                        writeToFile(saveName1, '\n')
                        #saveFile.write("\n")
                #saveFile.close()
                print(saveName + " is done.")
            print("Done")
            exit()
        else:
            for l in lines:
                if l != "":
                    try:
                        t = l if l.isdigit() or l.isdecimal() else translator.translate(l, "", langKey)
                    except Exception:
                        try:
                            t = l if l.isdigit() or l.isdecimal() else translator2.translate(text=l)
                        except Exception:
                            t = l if l.isdigit() or l.isdecimal() else mt.translate(l, source=languages.get(langdetect.detect(l)).capitalize(), target=languages.get(langKey).capitalize())
                    if "„" in t:
                        t = t.replace("„", '"')
                    writeToFile(saveName, t + '\n')
                    #saveFile.write(t + "\n")
                    print(l + " -> " + t)
                else:
                    writeToFile(saveName, '\n')
                    #saveFile.write("\n")
            #saveFile.close()
            print("Done")


def Extract(fileName: str, saveName: str):
    subs = pysubs2.load(fileName, encoding="utf-8", errors='ignore')
    textFile = open(saveName, 'a', encoding="utf-8")
    for line in subs:
        print(line.text)
        textFile.write(line.text + '\n')
    textFile.close()
    print('Extracted all text')


def Modify(fileName: str, saveName: str):
    subs = pysubs2.load(fileName, encoding="utf-8", errors='ignore')
    lines = []
    fileMod = open(saveName, encoding="utf-8")
    for l in fileMod:
        if '\n' in l:
            l = l.replace('\n', '')
        lines.append(l)
    ind = 0
    for line in subs:
        line.text = lines[ind]
        ind += 1
    subs.save(fileName)
    print('Saved modified version')


if __name__ == '__main__':
    while True:
        subs = input("Enter every .ass file you want to extract the text from (ex: test.ass,test1.ass): ")
        if subs != '':
            subs = subs.split(',') if ',' in subs else subs
            print()
            extractedFileNames = input(
                "Enter the names of the files in witch the extracted text is going to be saved as (ex: text.txt,text1.txt): ")
            if extractedFileNames != '':
                extractedFileNames = extractedFileNames.split(',') if ',' in extractedFileNames else extractedFileNames
                print()
                transFileNames = input(
                    "Enter the names of the files in witch the translated text is going to be saved as (ex: text.txt,text1.txt): ")
                if transFileNames != '':
                    transFileNames = transFileNames.split(
                        ',') if ',' in transFileNames else transFileNames
                    print()
                    transToAll = input("Translate to all languages (Y/N): ").lower()
                    if transToAll != "":
                        transToAll = True if transToAll == 'y' or transToAll == 'yes' else False
                        print()
                        allLangs()
                        lang = input("Enter the number of the lang >> ")
                        if lang != '':
                            lang = int(lang)
                            break

    if type(subs) == list and type(extractedFileNames) == list and type(transFileNames) == list:
        ind = 0
        for f in subs:
            Extract(fileName=f, saveName=extractedFileNames[ind])
            ind += 1
        ind = 0
        for ext in extractedFileNames:
            trans(fileName=ext, saveName=transFileNames[ind], translateToAllLangs=transToAll, langInd=lang - 1)
            ind += 1
        ind = 0
        for f in subs:
            Modify(fileName=f, saveName=transFileNames[ind])
            ind += 1
    else:
        Extract(fileName=subs, saveName=extractedFileNames)
        trans(fileName=extractedFileNames, saveName=transFileNames, translateToAllLangs=transToAll, langInd=lang - 1)
        Modify(fileName=subs, saveName=transFileNames)


