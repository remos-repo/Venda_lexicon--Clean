#developlist of unigrams from corpus with data cleaning in between -- removing + cleaning unicode errors
#import libraies
import argparse as ap
import nltk  
import json
from nltk import ngrams
from nltk.lm.preprocessing import pad_both_ends
import regex as re
import os
import unicodedata
import pandas as pd
import  argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, required=True,
                    help="provide path to corpus file of .txt and .csv files")
parser.add_argument("output", type=str, required=True,
                    help="provide output name without extension")
args = parser.parse_args()

#n_gram_generator() generates a N-gram lists and receives a list of tokens and the N value as a parameter 
def n_gram_generator(t: list, n_val:int):
    ngram_dict = {}
    #iterate through token list and create an ngram of each one
    for i in t:
        n_grams_list= list(ngrams(i, n=n_val, pad_left=True, pad_right=True, right_pad_symbol="</s>", left_pad_symbol="<s>"))
        
        for ngram in n_grams_list:
            ngram_dict[ngram] = ngram_dict.get(ngram,0)+1

    return ngram_dict #returns dict of counted value of ngrams, to be received as final_ngrams and calculate probabilities


n_value = 1
token_list=[]
ngrams_dict_list =[]

#path = "/home/ttl1/Venda_lexicon--Clean/messy_corpus"
path = f"{args.path}"

#file = "messy_corpus/thepresidency.csv"
for filename in os.listdir(path):
    #figure out where to open a file to write out the 
    full_path = os.path.join(path, filename)
    if os.path.isfile(full_path):
            print(f"File: {filename}")
#open training file and preprocess
#usually its full_path 
    with open (full_path, "r", encoding="utf-8") as f_input:
        text = f_input.read().strip()
        normalized_text = unicodedata.normalize("NFKC", text) #re.sub(r"\p{Pd}", "-", text)
        clean_text = re.sub(r"[^\s\p{L}]", ' ', normalized_text, flags=re.UNICODE)
        cleaner_text = clean_text.replace('\u200b', ' ').strip()
        sentence_tokens= nltk.sent_tokenize(cleaner_text)
        for sentence in sentence_tokens:
            tokens= nltk.word_tokenize(sentence)
            #tokens_with_padders = ["<s>"] + tokens + ["</s>"]
            token_list.append(tokens)
        print("token list created")
        print(len(token_list))
#clean my tokens

#create value for range
range_value = n_value+1
#error message for values outside the boundary of one to 6 unigrams
if ((n_value < 1) or (n_value>7)):
    print("N-grams from 1 to 6.")
else:
    for n in range(1, range_value):
        if n==1: #generate unigrams frequency list and update the ungrams frequency dictionary append to all list of N-gram dictionaries 

            unigrams =n_gram_generator(t=token_list, n_val=n)
            #unigrams = dict(sorted(unigrams.items(), key=lambda item: item[1], reverse=True))
            #print(unigrams)

            ngrams_dict_list.append(unigrams)

        else:
            n_gram_dict= n_gram_generator(token_list, n_val=5)
            n_gram_dict = dict(sorted(n_gram_dict.items(), key=lambda item: item[1], reverse=True))
            #ngrams_dict_list.append(n_gram_dict)

#split and sort words into uppercase and lowercase unigram dicts
upper_lexicon= {}
lower_lexicon= {}
for key, value in unigrams.items():
    word = key[0]
    if word[0].isupper() and (word.lower(),) not in unigrams:
        upper_lexicon.update({word:value})
    else:
        lower_lexicon.update({word.lower():value})

upper_lexicon= dict(sorted(upper_lexicon.items(), key=lambda item: item[1], reverse=True))
lower_lexicon= dict(sorted(lower_lexicon.items(), key=lambda item: item[1], reverse=True))

clean_data = {"upper lexicon": {}, "lower lexicon":{}}
clean_data["lower lexicon"].update(lower_lexicon)

clean_data["upper lexicon"].update(upper_lexicon)

output_file = f"{args.output}"
with open(f"{output_file}.json", "w", encoding="utf8") as out_file:
    json.dump(clean_data, out_file, indent=3, ensure_ascii=False)

#txt file to clean words using hunspell checker
with open(f"{output_file}.txt", "w", encoding="utf8") as out_file:
    n=1
    for k,v in lower_lexicon.items():
        out_file.write(f"{k}:\t{v}\n")
    n+=1


        