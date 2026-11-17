#clean data by using regex to find english lexicon in word list -- before or after clean_other_lang.py

import json
import regex as re
from nltk.corpus import words
import os
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, required=True,
                    help="provide path to input json file")
parser.add_argument("-c", "--case", required=True, type=str, choices=["lower", "upper"],
                    help="provide lower or upper to define the case of the lexicon")
parser.add_argument("-v", "--value", required=False, type=int, default=200,
                    help="provide value for the minimum frequency required to keep words from being removed from the list.")
parser.add_argument("output", type=str, required=True,
                    help="provide path to output json file without extension")
args = parser.parse_args()

#load nltk english word list
eng = words.words("en")
eng_lexicon = []
foreign_words=[]
for word in eng:
    if len(word) >3:
        eng_lexicon.append(word)
#print(eng_lexicon)
eng_lexicon.sort(key=len, reverse=True)
eng_lexicon_combined = "|".join(eng_lexicon)

#open file of dictionaries of foreign words
path = "./foreign_file"
for filename in os.listdir(path):
    full_path = os.path.join(path, filename)
    if os.path.isfile(full_path):
            print(f"File: {filename}")

    with open (full_path, "r", encoding="utf-8") as f_input:
        for line in f_input:
            de = line.strip()
            if len(de) >2:
                foreign_words.append(de)

corpus_file = f"{args.file}"
with open(corpus_file, "r", encoding="utf-8") as dict_in:
    sorted_corpus= json.load(dict_in)

lexicon_case = f"{args.case} lexicon"
#lexicon_case = "upper lexicon"
if lexicon_case in sorted_corpus: 
    lexicon = sorted_corpus[lexicon_case]
else:
    lexicon=sorted_corpus

error_terms = []
venda_lower_lexicon = {}
what_left = []
#match = re.search(eng_lexicon_combined)
#match word to englexicon, then search rest of word

#search dictionary for foreign word values
for word, val in lexicon.items(): 
    if word in eng_lexicon: #eng_lexicon:
        error_terms.append(word)
    elif word in foreign_words:
        error_terms.append(word)
    else:
        match= re.match(eng_lexicon_combined, word, re.IGNORECASE)    
        if match:
            remaining = word[match.end():]
            if re.search(eng_lexicon_combined, remaining, re.IGNORECASE):
                error_terms.append(word)
        elif re.fullmatch(eng_lexicon_combined, word, re.IGNORECASE):
            error_terms.append(word)    
        else:
            venda_lower_lexicon[word]=val


#filtered_dict = {k: v for k, v in venda_lower_lexicon.items() if k not in error_terms}
new_dict={}
shortwords=[]
freq_value = f"{args.value}"
#check frequency  of shorter words and keep those more frequent
for k,v in lexicon.items():
    if len(k)<= freq_value and k in error_terms:
        if v >200:
            shortwords.append(k)
            new_dict[k]=v
    if k in error_terms:
        pass
    else:
        new_dict[k]=v
print(f"what left: {shortwords}")
print(f"error terms {len(error_terms)}: {error_terms}")
output_file = f"{args.output}"
with open(f"{output_file}.json","w", encoding="utf-8") as outfile:
     json.dump(new_dict, outfile, ensure_ascii=False, indent=4)



