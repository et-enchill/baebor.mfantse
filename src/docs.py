import os
import csv
from time import sleep
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))

def read_data(abbrv: str, chapter:str) -> str:
    data_path = f"{dir_path}/data/{abbrv}"
    chapter_code = str(chapter).zfill(3)
    chapter_file = f"{data_path}/{abbrv}.{chapter_code}.csv"
    data = f"## Tsir {chapter}\n\n"
    with open(chapter_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            verse_no = str(row[0]).split(".")[-1]
            
            texts = []
            for i in range(1, len(row)-1):
                text = str(row[i]).strip().strip('"')
                texts.append(text)
            verse_text = ", ".join(texts)
            data += f"{verse_no}. {verse_text}\n"

    return data

    
def main():
    
    data_path = f"{dir_path}/docs"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        
    with open(f"{dir_path}/books.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            abbrv = row[1].strip()
            book_data = f"# {row[2].strip()}\n\n"
            chapters = row[4].strip()
            
            for chapter in range(1, int(chapters) + 1):
                data = read_data(abbrv, chapter)
                book_data += f"{data}\n"
                print("%s %s %s ...read!" % (datetime.now(), abbrv, chapter))
                sleep(5)
            
            book_file = f"{data_path}/{abbrv.lower()}.md"
            writer = open(book_file, 'w+', encoding='utf-8')
            writer.writelines(book_data)
            writer.close()
            print("%s %s ...written!" % (datetime.now(), abbrv))
    
        print("EVERYTHING...done!")
        
        

if __name__ == "__main__":
    main()