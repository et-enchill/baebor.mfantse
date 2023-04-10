import os
import csv


dir_path = os.path.dirname(os.path.realpath(__file__))

def main():
        
    with open(f"{dir_path}/books.csv", "r") as f:
        reader = csv.reader(f)
        book_data = ""
        for row in reader:
            print(row)
            abbrv = row[1].strip()
            book_data += f"- {row[2].strip()}: baebor/{abbrv.lower()}.md\n"
            book_file = f"{dir_path}/books.md"
            writer = open(book_file, 'w+', encoding='utf-8')
            writer.writelines(book_data)
            writer.close()
    
        print("EVERYTHING...done!")
        
        

if __name__ == "__main__":
    main()