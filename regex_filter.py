import regex as re
from pathlib import Path
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, required=True,
                    help="provide path to input file")

args = parser.parse_args()


#read the file
#create a dict of the keys
#find the regex values
#swap the key for the value pair /home/ttl1/Venda_lexicon/extracted.txt

symbol_dict = {"¼": "ḽ",
               "¹": "Ṱ",
               "¿":"ṅ",
               "¾": "ṱ",
               "½": "ṋ",
               "·":"Ḽ",
               "µ": "ḓ",
               "¶": "Ḓ",
               "»":"ḓ",
               "º":"Ṅ"}
line_count = 0
file = Path(f"{args.file}")
file_name = file.stem
output_file = f"{file_name}-diacritics.txt"
trans_table = str.maketrans(symbol_dict)
with open(output_file, "w", encoding="utf-8") as f_out:
    with open(file, "r", encoding="utf-8") as f_in:
        for line in f_in:
            line_count += 1
            line = line.strip()
            
            new_line = line.translate(trans_table)
            f_out.write(f"{new_line}\n")
            #print(f"{line_count}/91644")
        