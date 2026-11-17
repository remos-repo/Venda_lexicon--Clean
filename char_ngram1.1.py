#create vharacter ngrams from venda lowercase lexicon
#copy to address altestamentliche 

import json
from collections import Counter
from collections import OrderedDict
import pandas as pd
import pylcs

def padded_chars(n_max: int, k: str):
    pad_grams =[]
    for n in range(4, n_max+1):
        #padding = "_" * (n - 1)
        #padded_k = padding + k + padding
        grams = [k[i:i+n] for i in range(len(k)-n+1)]
        #sliced_grams = grams[1:len(grams)-1]
        pad_grams.extend(grams)
    return pad_grams

def filter_words(char_list: list, not_vocab: list):
    for w in not_vocab:
        vocab_list =[]
        w_chars = padded_chars(n_size, w)#[padded_w[i:i+n] for i in range(len(padded_w)-n+1)]
        if all(gram in char_list for gram in w_chars):
            vocab_list.append(w)
        else:
            not_list.append(w)
        
    return vocab_list    

with open("clean_venda_lex1.json", "r", encoding="utf-8") as infile:
    venda_dict= json.load(infile)

#venda_dict = venda_dict.str.pad
lex_words = []

with open("clean_venda_lex2.txt", "r", encoding="utf-8") as inf:
    for line in inf:
        lex = line.strip()
        lex_words.append(lex)

words = venda_dict["lower lexicon"]

# Source - https://stackoverflow.com/a/18658215
# Posted by NPE
# Retrieved 2026-04-15, License - CC BY-SA 3.0

n_size = 4
char_ngrams =[]
full_vocab_list =[]
not_list =[]

for k, v in words.items():
    if v >=100:
        chars = padded_chars(n_size, k)        
        char_ngrams.extend(chars)
        full_vocab_list.append(k)

vocab = filter_words(char_ngrams, lex_words)

if vocab is not None:
    full_vocab_list.extend(vocab)
    new_chars = padded_chars(vocab)
    char_ngrams.extend(new_chars)
    


#['stud', 'tude', 'uden', 'dent']
#print(char_ngrams)
#freq_grams = Counter(char_ngrams)
#change value to prob : value over vocabulary

 
#order_grams= dict(sorted(freq_grams.items(), key=lambda item: item[1], reverse=True))

#prob_grams = {k:v/len(order_grams) for k,v in order_grams.items()} #sort char-grams as sorted probability grams



# compare venda lower lex to char-grams to create larger lexicon list

#recursively go through 3-grams/4-grams and they must all be in the list before adding to vocab

    #n_size+=1
            


print(not_list)
with open("not_list.txt", "w", encoding="utf-8") as outfile:
    for v in not_list:
        outfile.write(f"{v}\n")