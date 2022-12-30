import os

try:
    from google_translate_py import Translator
    import deep_translator as deep
    import dl_translate as dlt
    import langdetect
except ImportError:
    if os.name.startswith('win'):
        os.system("python -m pip install google-translate.py deep_translator dl-translate langdetect")
    else:
        os.system("python3 -m pip install google-translate.py deep_translator dl-translate langdetect")
    try:
        from google_translate_py import Translator
        import deep_translator as deep
        import dl_translate as dlt
        import langdetect
    except ImportError:
        print("Try installing google-translate.py with pip or try to install python 3.4+")
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

while True:
    fileName = input("Enter the name of the file or the location (example: text.txt | D:/MyFolder/text.txt) >> ")
    if fileName != "":
        print("")
        isTheFileConfig = input("Is the file a config file? Y/N >> ")
        isTheFileConfig = isTheFileConfig.lower()
        print("")
        if isTheFileConfig == "y" or isTheFileConfig == "yes" or isTheFileConfig == "da":
            isTheFileConfig = True
            allLangs()
            lang = input(
                "Enter the number of the language you want to translate to | If you want to translate it to all languages then whatever you enter here won't count. You will be asked later for this >> ")
            if lang != "":
                print("")
                outputFileName = input(
                    "Enter the file name or the path where you want the file to be saved (example: text.txt | D:/MyFolder/text.txt) >> ")
                if outputFileName != "":
                    print("")
                    translateToAllLangs = input("Do you want to translate it to all languages? Y/N >> ")
                    translateToAllLangs = translateToAllLangs.lower()
                    if translateToAllLangs == "y" or translateToAllLangs == "yes" or translateToAllLangs == "da":
                        translateToAllLangs = True
                        print("")
                        break
                    elif translateToAllLangs == "n" or translateToAllLangs == "no" or translateToAllLangs == "ne":
                        translateToAllLangs = False
                        print("")
                        break

        elif isTheFileConfig == "n" or isTheFileConfig == "no" or isTheFileConfig == "ne":
            isTheFileConfig = False
            allLangs()
            lang = input("Enter the number of the language you want to translate to >> ")
            if lang != "":
                print("")
                outputFileName = input(
                    "Enter the file name or the path where you want the file to be saved (example: text.txt | D:/MyFolder/text.txt) >> ")
                if outputFileName != "":
                    print("")
                    translateToAllLangs = input("Do you want to translate it to all verbalise languages? Y/N >> ")
                    translateToAllLangs = translateToAllLangs.lower()
                    if translateToAllLangs == "y" or translateToAllLangs == "yes" or translateToAllLangs == "da":
                        translateToAllLangs = True
                        print("")
                        break
                    elif translateToAllLangs == "n" or translateToAllLangs == "no" or translateToAllLangs == "ne":
                        translateToAllLangs = False
                        print("")
                        break

def getLang():
    global lang
    lang = int(lang) - 1
    KEYS = []
    for key in languages:
        KEYS.append(key)
    return KEYS[lang]

def trans():
    global outputFile, translator2, timeoutMessage, mt
    langKey = getLang()
    if isTheFileConfig:
        # The file IS CONFIG
        lines = []

        for line in file:
            lines.append(line)

        if translateToAllLangs:
            newName = ""
            for char in outputFileName:
                if char == ".":
                    break
                else:
                    newName += char
            fileType = ""
            done = False
            for char in outputFileName:
                if char == "." or done:
                    fileType += char
                    done = True
            for key in languages.keys():
                outputFile = open(newName + "-" + key + fileType, "a")
                for l in lines:
                    if l != "":
                        done = False
                        word = ""
                        for char in l:
                            if char == ":" or done:
                                word += char
                                done = True
                        try:
                            t = word if word.isdigit() or word.isdecimal() else translator.translate(word, "", key)
                        except Exception:
                            try:
                                translator2 = word if word.isdigit() or word.isdecimal() else deep.GoogleTranslator(source="auto", target=key)
                                t = word if word.isdigit() or word.isdecimal() else translator2.translate(text=word)
                            except Exception:
                                t = word if word.isdigit() or word.isdecimal() else mt.translate(word, source=languages.get(langdetect.detect(word)).capitalize(), target=languages.get(key).capitalize())
                        if "„" in t:
                            t = t.replace("„", '"')
                        newLine = l.replace(word, t)
                        outputFile.write(newLine+"\n")
                        print(l + " -> " + newLine)
                    else:
                        outputFile.write("\n")
                outputFile.close()
                print(outputFile.name + " is done.")
            print("Done")
            exit()
        else:
            for l in lines:
                if l != "":
                    done = False
                    word = ""
                    for char in l:
                        if done:
                            word += char
                        if char == " ":
                            done = True
                    try:
                        t = word if word.isdigit() or word.isdecimal() else translator.translate(word, "", langKey)
                    except Exception:
                        try:
                            t = word if word.isdigit() or word.isdecimal() else translator2.translate(text=word)
                        except Exception:
                            t = word if word.isdigit() or word.isdecimal() else mt.translate(word, source=languages.get(langdetect.detect(word)).capitalize(), target=languages.get(langKey).capitalize())
                    if "„" in t:
                        t = t.replace("„", '"')
                    newLine = l.replace(word, t)
                    outputFile.write(newLine+"\n")
                    print(l + " -> " + newLine)
                else:
                    outputFile.write("\n")
            outputFile.close()
            print("Done")
            exit()
    else:
        # the file is NOT CONFIG
        lines = []
        for line in file:
            if "\n" in line:
                line = line.replace("\n", "")
            lines.append(line)
        if translateToAllLangs:
            for key in languages.keys():
                newName = ""
                for char in outputFileName:
                    if char == ".":
                        break
                    else:
                        newName += char
                fileType = ""
                done = False
                for char in outputFileName:
                    if char == "." or done:
                        fileType += char
                        done = True
                outputFile = open(newName + "-" + key + fileType, "a")
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
                        outputFile.write(t+"\n")
                        print(l + " -> " + t)
                    else:
                        outputFile.write("\n")
                outputFile.close()
                print(outputFile.name + " is done.")
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
                    outputFile.write(t+"\n")
                    print(l + " -> " + t)
                else:
                    outputFile.write("\n")
            outputFile.close()
            print("Done")


if __name__ == '__main__':
    file = open(fileName, "rt")
    if not (translateToAllLangs):
        outputFile = open(outputFileName, "a")
    translator = Translator()
    mt = dlt.TranslationModel()
    translator2 = deep.GoogleTranslator(source='auto', target=getLang())
    timeoutMessage = "Too much requests. Timeout! Try again soon..."
    trans()

