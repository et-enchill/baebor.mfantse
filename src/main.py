from time import sleep
from datetime import datetime
import requests, csv
from bs4 import BeautifulSoup

def prepare_soup(abbrv, chapter):
    base_url = "https://www.bible.com/bible/2914/%s.%s.MFANBRPC" % (abbrv, chapter)
    headers = {
        'User-Agent': 'Mozilla/5.0',
    }
    req = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup

def save_data(abbrv, chapter, data):
    csv_data = ""
    for item in data:
        csv_data += "\"%s\", \"%s\", \"%s\"\n" % (item['code'], item['content'], item['note'])
        # print(item)
        
    chapter_code = "C%s" % str(chapter).zfill(3)
    chapter_file = "data/{0}/{0}.{1}.txt".format(abbrv, chapter_code)
    clean = open(chapter_file, 'w+', encoding='utf-8')
    clean.writelines(csv_data)
    clean.close()


def clean_data(data):
    data.strip()
    data_list = data.split("\n")
    clean_list = []
    for item in data_list:
        item.replace("&#8217;", "'")
        clean_list.append(item.strip())
        
    return ''.join(clean_list)
        

def scrap_data(abbrv, chapter):
    soup = prepare_soup(abbrv, chapter)
    verses_span = soup.find_all("span", {"data-usfm" : True})

    verses = {}
    for i in range(0, len(verses_span) -1):
        verse_div = verses_span[i]
        
        if not bool(len(verse_div.text.strip()) > 0):
            continue
        
        # Code
        code = verse_div.attrs['data-usfm']
        node = code.replace('.', '')
        num = code.split('.')[-1]
        #print(code)
        
        contents_span = verse_div.find_all("span", class_="content")
        content = ""
        for content_span in contents_span:
            content += content_span.text.strip() + " "
      
        
        notes_span = verse_div.find_all("span", class_="note")
        note = ""
        for note_span in notes_span:
            note += note_span.text.strip() + " "
            
        note = clean_data(note)
        content = clean_data(content)
                
        if not node in verses:
            verses[node] = {
                'code': num.strip(),
                'note': note.strip(),
                'content': content.strip(),
            }
        else:
            verses[node] = {
                'code': num.strip(),
                'note': verses[node]['note'].strip() + " " + note.strip(),
                'content': verses[node]['content'].strip() + " " + content.strip(),
            }
            
        
    return verses    
    


def main():
    with open("jamrev.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
                    
            abbrv = row[1].strip()
            chapters = row[4].strip()
            for chapter in range(1, int(chapters) + 1):
                data = scrap_data(abbrv, chapter)
                save_data(abbrv, chapter, data.values())
                print("%s %s %s ...done!" % (datetime.now(), abbrv, chapter))
                sleep(5)
                
        print("...done!")
    
    
def book():
    abbrv = "HEB"
    chapters = 13
    for chapter in range(1, int(chapters) + 1):
        data = scrap_data(abbrv, chapter)
        save_data(abbrv, chapter, data.values())
        print("%s %s %s ...done!" % (datetime.now(), abbrv, chapter))
        sleep(5)
        
        
    print("...done!")
    
    
if __name__ == "__main__":
    main()