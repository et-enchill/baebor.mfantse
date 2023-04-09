import os, json, csv


def clean_verses_json(data, opt):
    verses = []
    for row in data:
        part = opt['part']
        book_id = opt['book_id']
        book_code = opt['book_code']
        chapter = opt['chapter']
        num = row[0]
        message = row[1]
        notes = row[2]
        
        chapter_code = "C%s" % str(chapter).zfill(3)
        code = "%s.%s.V%s" % (book_code, chapter_code, str(num).zfill(3))
        verse = {
            "part": part,
            "book_id":book_id,
            "chapter": int(chapter),
            "number": num,
            "code": code,
            "message": message,
            "notes": notes
        }
        verses.append(verse)

    return verses


def get_chap_json(book_abbrv, chapter):
    chap_code = "C%s" % str(chapter).zfill(3)
    data_path = "data/{0}/{0}.{1}.txt".format(book_abbrv, chap_code)
    # data_loc = os.path.join(settings.BASE_DIR, data_path)
    data = None
    with open(data_path, 'r') as file:
        data = csv.reader(file)
        
    return data


def main():
    abbrv = "GEN"
    chapter = 14
    chapter_code = "C%s" % str(chapter).zfill(3)
    chapter_file = "data/{0}/{0}.{1}.txt".format(abbrv, chapter_code)
    
    with open(chapter_file, "r") as f:
        data = f.readlines()
        reader = csv.reader(data, quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            print(row)
                    
            # part = row[0]
            # abbrv = row[1].strip()
            # chapters = row[4].strip()
            # for chapter in range(1, int(chapters) + 1):
            #     data = scrap_data(abbrv, chapter)
            #     save_data(abbrv, chapter, data.values())
            #     print("%s %s %s ...done!" % (datetime.now(), abbrv, chapter))
            #     sleep(5)
                
        print("...done!")
    
    
    
if __name__ == "__main__":
    main()