#clean data based on ngrams of top 100 most frequent words (works the best for sure)
import json
import regex as re
import unicodedata


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
    #difference = len(word_set) - len(intersect_set)
    #for m in range(8, 4, -1):
    #if all(gram in char_grams for gram in word_grams):
    #    return True
    #if all(word_grams) in char_grams:
    if len(intersect_set) <= m_int:
        return True 
    else:
        return False
    #if more than m_int char-grams are missing then its likely not a word?

with open("clean_noforeign_dict2.3.json", "r", encoding="utf-8") as infile:
    lower_lex= json.load(infile)

#lower_lex = venda_dict["lower lexicon"]

chars_list =[]
venda_list = []

for k, v in lower_lex.items():
    if v >=100:
        venda_list.append(k)
        chars = create_char_grams(nmin=2, nmax=5, word=k)   
        chars_list.extend(chars) #extend list of char-grams from chars of word with freq over 100

not_venda =[]       

#lex_words = [] 

#read cleanest version of list of words
# with open("clean_venda_lex2.txt", "r", encoding="utf-8") as inf:
#      for line in inf:
#          lex = line.strip()
#          lex_words.append(lex)


#bad_stuff = re.compile("\p{Lm}", re.UNICODE)
full_vocab= []
diacrits = ["ḽ","ṅ","ṱ","ṋ","ḓ"]
non_diactitics =r"[aeiouAEIOU]\p{M}*"
vidiowords=[]
char_match = re.compile(r"[^a-zA-Zḽṅṱṋḓ]")
vid_match = re.compile(r"vidio[a-zA-Zḽṅṱṋḓ]+")
#go through list of cleanest lex, create ngrams add valid matches to list of char-grams
for j in range(5, 2, -1):
   for w,v in lower_lex.items():
            if char_match.search(w):
                not_venda.append(w)
            elif vid_match.search(w):
                not_venda.append(w)
            else:  
                match=False
                w_chars = create_char_grams(nmin=j, nmax=j, word=w)
                #for m in range(9,5,-1):
                match = filter_words(chars_list, w_chars,3)
                #if its a match that means there are less than m_int interesecting words with common venda char-grams so its probably not a venda word
                if match == True:
                    not_venda.append(w)
                else:
                    chars_list.extend(w_chars)
                    full_vocab.append(w)
                #lex_words.remove(w)


lemme_see = sorted(set(not_venda))
full_vocab= sorted((set(full_vocab)))
#lemme_see2 = []
print(lemme_see)
print(len(lemme_see))
new_dict={}
for k,v in lower_lex.items():
    if k not in lemme_see:
        pass
    elif k in vidiowords:
        pass
    else:
        new_dict[k]=v
#new_venda_dict = {k:v for k, v in words.items() if k not in lemme_see2 or vidiowords}
#lower_lex=final_venda_dict["lower lexicon"]

with open("curoious4intersects.json", "w", encoding="utf-8") as outf:
    json.dump(new_dict, outf, ensure_ascii=False, indent=4)
