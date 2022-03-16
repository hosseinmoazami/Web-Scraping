from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import csv
from pathlib import Path
import json


def extractWords():
    print("On Words Working...")
    html_doc = requests.get(URL)
    parser = BeautifulSoup(html_doc.content, 'html.parser')
    cards = parser.find_all("div", {'class': 'side front'})
    words = []

    for item in cards:
        ID = re.findall(r"'(.*?)'", item['onclick'], re.DOTALL)[0]
        word = item.find("td").string.split(", ")
        plural = ""
        if 1 < len(word): plural = word[1]
        my_obj = {"ID": ID, "word": word[0], "plural": plural}
        words.append(my_obj)
    # print(json.dumps(words, indent = 4) )
    return words


def saveWordOnCSV(list):
    print("Words Saved...")

    with open(path + "/lektion_" + Lektion + '/words.csv', 'w') as file:
        header = ['Word', 'English', 'Sentence', 'Plural']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for item in list:
            writer.writerow({
                'Word': item["word"],
                'English': ' ',
                'Sentence': ' ',
                'Plural': item["plural"]
            })


def downloadVoice(list):
    print("On Voice Downloading...")

    for item in list:
        file = path + "/lektion_" + Lektion + "/voice/" + item["ID"] + ".mp3"
        voice_path = voice_url + item["ID"] + ".mp3"
        urllib.request.urlretrieve(voice_path, file)

    print("Voice Saved...")


Level = input("Enter Level Number EX(A1): ")
Lektion = input("Enter Lektion Number EX(01): ")
print("Download Lektion (" + Lektion + ") of Level (" + Level + ")")

URL = 'https://startenwir.com/card' + Level + '_' + Lektion + '.html'
voice_url = "https://startenwir.com/assets/aud/" + Level.lower(
) + "/" + Lektion + "/"
path = "./" + Level

print("Cerate Directories...")
Path(path).mkdir(parents=True, exist_ok=True)
Path(path + "/lektion_" + Lektion).mkdir(parents=True, exist_ok=True)
Path(path + "/lektion_" + Lektion + "/voice").mkdir(parents=True,
                                                    exist_ok=True)

list_of_words = extractWords()
saveWordOnCSV(list_of_words)
downloadVoice(list_of_words)