import json
import regex as re

with open("char2.1_words_clean.json", "r", encoding="utf-8") as infile:
    venda_dict= json.load(infile)

char_match = re.compile(r"[^a-zA-Zḽṅṱṋḓ]")
vid_match = re.compile(r"vidio[a-zA-Zḽṅṱṋḓ]+")
not_word=[]
words = []
for k, v in venda_dict.items():
    if char_match.search(k):
        not_word.append(k)
    elif vid_match.search(k):
        not_word.append(k)
    else:
        words.append(k)
    
print(not_word)

words_to_keep = {k:v for k,v in venda_dict.items() if k not in not_word}

with open("cleanest_word_list.json", "w", encoding="utf-8") as outf:
    json.dump(words_to_keep, outf, indent=4, ensure_ascii=False)