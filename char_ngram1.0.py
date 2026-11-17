#create vharacter ngrams from venda lowercase lexicon
import json
from collections import Counter
from collections import OrderedDict
with open("clean_venda_lex1.json", "r", encoding="utf-8") as infile:
    venda_dict= json.load(infile)

words = venda_dict["lower lexicon"]

# Source - https://stackoverflow.com/a/18658215
# Posted by NPE
# Retrieved 2026-04-15, License - CC BY-SA 3.0

n_size = 4
char_ngrams =[]


for k, v in words.items():
    if v >=100:
        for n in range(2, n_size+1):
            chars= [k[i:i+n] for i in range(len(k)-n+1)]
            char_ngrams.extend(chars)
        #i+=1
#['stud', 'tude', 'uden', 'dent']
#print(char_ngrams)
freq_grams = Counter(char_ngrams)
#change value to prob : value over vocabulary

 
order_grams= dict(sorted(freq_grams.items(), key=lambda item: item[1], reverse=True))

prob_grams = {k:v/len(order_grams) for k,v in order_grams.items()}
#dict_gram = dict(sorted(freq_grams.items(), key=lambda item: item[1]))
with open("char-ngrams-probabilities.json", "w", encoding="utf-8") as outf:
    json.dump(prob_grams,outf, ensure_ascii=False, indent=2)

vocab_list =[]
not_list =[]
# compare venda lower lex to char-grams to create larger lexicon list

for w in words:
    if any(gram in w for gram in order_grams):
        vocab_list.append(w)
    else:
        not_list.append(w)


# for case, lex in venda_dict.items():
#     for w in lex.keys():
#         if any(gram in w for gram in order_grams):
#         #for gram in order_grams.keys():
#             #if gram in w:
#                 vocab_list.append(w)
#         else:
#             not_list.append(w)

print(not_list)
with open("char-vocab-full.txt", "w", encoding="utf-8") as outfile:
    for v in vocab_list:
        outfile.write(f"{v}\n")