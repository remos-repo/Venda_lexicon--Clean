import json
import regex as re
import unicodedata
from collections import Counter
from pathlib import Path
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, required=True,
                    help="provide path to input json file that will be cleaned")
parser.add_argument("wordlist", type=str, required=True,
                    help="provide path to word list to create clean ngrams as a json file. Can be the same as input file")
parser.add_argument("-c", "--case", required=True, type=str, choices=["lower", "upper"],
                    help="provide lower or upper to define the case of the lexicon")
parser.add_argument("-v", "--value", required=False, type=int, default=100,
                    help="provide value for the minimum frequency required to keep words from being removed from the list.")
parser.add_argument("output", type=str, required=True,
                    help="provide path to output json file")
args = parser.parse_args()

def create_char_grams(nmin: int, nmax:int, word: str):
    grams_list = []
    for n in range(nmin, nmax+1):
        padding = "_" * (n - 1)
        padded_k = padding + word + padding
        grams = [padded_k[i:i+n] for i in range(len(padded_k)-n+1)]
        grams_list.extend(grams)
    return grams_list #return list of char grams of word

def filter_words(char_grams, word_grams, m_int):
    word_set = set(word_grams)
    char_set = set(char_grams)
    intersect_set =  word_set & char_set
    if len(intersect_set) <= m_int:
        return True 
    else:
        return False
    #if more than m_int char-grams are missing then its likely not a word?

file_name = Path(args.wordlist)
with open(file_name, "r", encoding="utf-8") as infile:
    word_list= json.load(infile)

dirty_lexicon = Path(f"{args.file}")
with open(dirty_lexicon, "r", encoding="utf-8") as infile:
    sorted_corpus= json.load(infile)

lexicon_case = f"{args.case} lexicon"
#lexicon_case = "upper lexicon"
if lexicon_case in sorted_corpus: 
    lexicon = sorted_corpus[lexicon_case]
else:
    lexicon=sorted_corpus

chars_list =[]
venda_list = []
not_venda =[]
#regex patterns for filtering out data.
char_match = re.compile(r"[^a-zA-Zḽṅṱṋḓ]")
vowel_match = re.compile(r"a|e|i|o|u")
vid_match = re.compile(r"vidio[a-zA-Zḽṅṱṋḓ]+|c|j")

freq_val = f"{args.value}"
#create ngrams from wordlist file
for k, v in word_list.items():
        if v >=freq_val:
            venda_list.append(k)
            chars = create_char_grams(nmin=2, nmax=4, word=k)   
            chars_list.extend(chars) #extend list of char-grams from chars of word with freq over 100

#detect words 
full_vocab= []
vidiowords=[]

#go through list of cleanest lex, create ngrams add valid matches to list of char-grams
for j in range(4, 2, -1):
   for w,v in lexicon.items():
        w_low = w.lower() 
        if char_match.search(w_low):
                not_venda.append(w)
        elif vid_match.search(w_low):
                not_venda.append(w)
        elif len(w_low)<4 and not vowel_match.search(w_low):
             not_venda.append(w)
        else: 
                match=False
                w_chars = create_char_grams(nmin=j, nmax=j, word=w_low)
                #for m in range(9,5,-1):
                match = filter_words(chars_list, w_chars,4)
                #if its a match that means there are less than m_int interesecting words with common venda char-grams so its probably not a venda word
                if match == True:
                    not_venda.append(w)
                else:
                    #chars_list.extend(w_chars)
                    full_vocab.append(w)
                #lex_words.remove(w)


lemme_see = sorted(set(not_venda))
full_vocab= sorted((set(full_vocab)))
#see what words are being removed to confirm its not removing too much information
print(lemme_see)
print(len(lemme_see))
new_dict={}
for k,v in lexicon.items():
    if k in lemme_see:
        pass
    elif k in vidiowords:
        pass
    else:
        new_dict[k]=v
output_file = f"{args.output}"
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(new_dict, outfile, ensure_ascii=False, indent=4)
