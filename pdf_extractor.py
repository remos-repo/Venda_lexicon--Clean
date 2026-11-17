import os
import pdfplumber
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, required=True,
                    help="provide path to pdf files")

args = parser.parse_args()

#extract words from pdf and append to one long extracted file

path = f"{args.path}"
for filename in os.listdir(path):
    #figure out where to open a file to write out the 
    full_path = os.path.join(path, filename)
    with open("./extracted-text.txt", "a", encoding="utf-8") as out_file:
        if os.path.isfile(full_path):
            print(f"File: {filename}")
            text = ""
            with pdfplumber.open(full_path) as pdf:
               for page in pdf.pages:
                   #Extract text, layout=True helps keep formatting
                    text += page.extract_text()
                    text.encode("utf-8", "ignore")
            print(text)

            out_file.write(f"{text}\n")
        elif os.path.isdir(full_path):
            print(f"Directory: {filename}")
