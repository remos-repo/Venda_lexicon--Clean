#detect words from other languages using extracted words and chargrams from the venda lex list using hunspell
import regex as re
import pandas as pd
from nltk.corpus import words

import json 

def create_char_grams(nmin: int, nmax:int, word: str):
    grams_list = []
    for n in range(nmin, nmax+1):
        padding = "_" * (n - 1)
        padded_k = padding + word + padding
        grams = [padded_k[i:i+n] for i in range(len(padded_k)-n+1)]
        grams_list.extend(grams)
    return grams_list #return list of char grams of word

#filter chargrams and wordsgrams, if less than 12 inersecting grams occur its probably not a venda word
def filter_words(char_grams, word_grams):
    try_set = set(char_grams) & set(word_grams)
    if all(gram in char_grams for gram in word_grams):
        return True
    #elif len(try_set) >= 12:
        #return True
    else:
        return False

#read word lists and append them to a list of foreign words
foreign_words =[]
eng = words.words("en-basic")
eng_lexicon = []
for word in eng:
    if len(word) >=5:
        foreign_words.append(word)

with open("de_words.txt", "r", encoding="utf-8") as de_file:
    for line in de_file:
        de = line.strip()
        foreign_words.append(de)

with open("FR_words.txt", "r", encoding="utf-8") as fr_file:
    for line in fr_file:
        fr = line.strip()
        foreign_words.append(fr)

with open("eng_words.txt", "r", encoding="utf-8") as eng_file:
    for line in eng_file:
        fr = line.strip()
        foreign_words.append(fr)

#read dict 
with open("sorted_corpus_no_khandiso.json", "r", encoding="utf-8") as inf:
    venda_dict=json.load(inf)

#foreing_exp = "|".join(foreign_words)
lower_lexicon = venda_dict["lower lexicon"]
venda_word = []
        
        
#create germ char-grams 4-5 letters
char_ngrams =[]
vocab_list =[]
not_list =[]

for k in foreign_words:
    if len(k) >4:
        #venda_list.append(k)
        chars = create_char_grams(nmin=3, nmax=4, word=k)   
        char_ngrams.extend(chars)
char_match = re.compile(r"[^a-zA-Zḽṅṱṋḓ]")

short_words = []
for j in range(4, 3, -1):
    for w,v in lower_lexicon.items():
        if len(w) < 3 and v > 200:
            vocab_list.append(w)
        elif char_match.search(w):
            not_list.append(w)
        else:
            match=False
            w_chars = create_char_grams(nmin=j, nmax=j, word=w)
            match = filter_words(char_ngrams, w_chars)
            
            if match == True:
                char_ngrams.extend(w_chars)
                not_list.append(w)
                #venda_word.remove(w)
            else:
                vocab_list.append(w)
            
#matches = {f_w:{w:find_LCS(f_w, w) for w in venda_word if len(find_LCS(w,f_w))>3} for f_w in foreign_words}
new_dict ={}
# maybe_eng = []
# for word in not_list:
#     if len(w) <5:
#         if w not in foreign_words:
#             short_words.append(w)
#         else:
#             maybe_eng.append(w)
#     else:
#         pass
# print(f"might be venda: {short_words}\n not venda: {maybe_eng}")
lemme_see = sorted(list(set(not_list)))
#print(lemme_see)
print(len(lemme_see))
for w, v in lower_lexicon.items(): 
    if w in lemme_see:
        pass
    else:
        new_dict[w]=v

#print(matches)

with open("clean_other_langs5.json", "w", encoding="utf8") as out_file:
     json.dump(new_dict, out_file, indent=3, ensure_ascii=False)

