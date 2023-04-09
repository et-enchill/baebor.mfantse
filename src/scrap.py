import os
import csv
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup

dir_path = os.path.dirname(os.path.realpath(__file__))

def prepare_soup(abbrv, chapter):
    base_url = "https://www.bible.com/bible/2914/%s.%s.MFANBRPC" % (abbrv, chapter)
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    req = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def save_data(abbrv:str, chapter:str, data:dict):
    csv_data = ""
    for item in data.values():
        csv_data += f"\"{item['code']}\", \"{item['text']}\", \"{item['note']}\"\n"
        # print(item)
        
    
    data_path = f"{dir_path}/data/{abbrv}"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    
    chapter_code = str(chapter).zfill(3)
    chapter_file = f"{data_path}/{abbrv}.{chapter_code}.csv"
    clean = open(chapter_file, 'w+', encoding='utf-8')
    clean.writelines(csv_data)
    clean.close()


def clean_data(data:str):
    data.strip()
    data_list = data.split("\n")
    clean_list = []
    for item in data_list:
        item.replace("&#8217;", "'")
        clean_list.append(item.strip())
        
    return ''.join(clean_list)
        

def scrap_data(abbrv:str, chapter:str):
    soup = prepare_soup(abbrv, chapter)
    verses_span = soup.find_all("span", {"data-usfm" : True})
    verses_len = len(verses_span)

    verses = {}
    for i in range(0, verses_len):
        verse_div = verses_span[i]
        
        if not bool(len(verse_div.text.strip()) > 0):
            continue
        
        contents_text, contents_note = [], []
        for content in verse_div.contents:
            if isinstance(content.string, str):
                contents_text.append(content.text)
            else:
                contents_note.append(content.text)
        
        if not contents_text:
            continue
        
        # content = verse_div.contents[-1]
        code = str(verse_div.attrs['data-usfm']).strip()
        text = clean_data(" ".join(contents_text))
        num = code.split('.')[-1]
        text = str(text.lstrip(num)).strip()
        note = clean_data(" ".join(contents_note)) if contents_note else None
        if not code in verses:
            verses[code] = {
                "code": code,
                "text": text,
                "note": note if note else ""
            }
        else:
            verses[code]['text'] += " " + text
            if note:
                verses[code]['note'] += " " + note

    return verses    
    


def main():
    with open(f"{dir_path}/books.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
                    
            abbrv = row[1].strip()
            chapters = row[4].strip()
            status = int(row[5].strip())
            if status == 0:
                for chapter in range(1, int(chapters) + 1):
                    data = scrap_data(abbrv, chapter)
                    save_data(abbrv, chapter, data)
                    print("%s %s %s ...done!" % (datetime.now(), abbrv, chapter))
                    sleep(5)
            else:
                print("%s %s ...already done!" % (datetime.now(), abbrv))
                
        print("EVERYTHING...done!")
    
    
def book():
    abbrv = "JOL"
    chapters = 3
    for chapter in range(3, int(chapters) + 1):
        data = scrap_data(abbrv, chapter)
        save_data(abbrv, chapter, data)
        print("%s %s %s ...done!" % (datetime.now(), abbrv, chapter))
        sleep(5)
        
        
    print("...done!")
    
    
if __name__ == "__main__":
    main()