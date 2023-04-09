import csv

# https://www.bible.com/bible/2914/GEN.1.MFANBRPC

part = "T01"
book_code = "T01.B01"
chapter = 1
chapter_code = "C001"
source = "gen"


def clean_data():
    data = ''
    with open("%s.txt" % source, 'r') as file:
        data = file.read()
    
    lines, line, num = [], "", ""
    for i in range(len(data) -1):
        if bool(data[i].isnumeric()):
            num += data[i]            
            line = ""
        else:
            line += data[i]
            if bool(data[i+1].isnumeric()):
                code = "%s.%s.V%s" % (book_code, chapter_code, str(num).zfill(3))
                verse = "%s  %s %s\n" % (num, code, line)
                lines.append(verse)
                line = ""
                num = ""

    clean = open("%s.csv" % source, 'w')
    clean.writelines(lines)
    clean.close()
    print("done...")
        
        
        
# clean_data()

def create_empty_file(source):
    file = open("data/%s.txt" % source, 'w')
    file.close()
    print("done...")
    
    
def create_chapter_code():
  
    file =  open("books.csv")
    csvreader = csv.reader(file)

    for items in csvreader:
        code = items[1].strip()
        chapters = items[4].strip()
        for i in range(0, int(chapters)):
            chapter_code = "%s.C%s" % (code, str(i+1).zfill(3))
            create_empty_file(chapter_code)
            
        # chapter_code = "%s%s" % (code.upper(), str(chapters).zfill(3))
        # print(chapter_code)
    
    #return chapter_code
    
create_chapter_code()