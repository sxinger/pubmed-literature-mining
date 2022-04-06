import os
import nltk 
import re
import json
import string
from nltk.corpus import stopwords

# need to download nltk resources
#-- only need to download once as along saving to the same directory
#-- current default folder: ...AppData\Roaming\nltk_data
# nltk.download('punkt')
# nltk.download('stopwords')
nltk.download('popular')

# specify path to file
fn = 'als-mnd-risk-factor-ab'
abspath_fn = f'{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}\\data\\{fn}.txt'

def clean_text(txt:list):
    # convert to all lower cases
    txt = [w.lower() for w in txt]
    # remove punctuation
    txt = [w for w in txt if w not in string.punctuation]
    # remove numbers
    txt = [w for w in txt if not (w.isdigit() or w[0] == '-' and w[1:].isdigit() or w.split('.')[0].isdigit() or w.split(',')[0].isdigit())]
    # strip stemmer
    # txt = [nltk.PorterStemmer().stem(t) for t in txt] -- distort regular word
    # remove stop words
    txt = [w for w in txt if w not in set(stopwords.words('english'))]
    return(txt)

# line-by-line parsing and tokenization
pmid_ab = {} #{pmid: '' ; ab_token: []}
sec_idx = 0
line_idx = 0
ab_ind = False 
with open(abspath_fn, 'r', encoding = 'utf-8') as f:
    for line in f:
        line_idx += 1
        # "^PMID-" marks the line of PMID, which is usually the starting point of a lit section
        if re.match('^(PMID-)+',line) and not ab_ind:
            sec_idx += 1
            # get PMID
            pmid = re.sub('(PMID-)','',line).strip()
            line_start = line_idx
            # initialize token vector
            ab_tokens = []
        # "TI  -" marks the line of title
        # elif re.match('^(TI  -)',line) and not ab_ind:
        #     ab_tokens.append(nltk.word_tokenize(re.sub('(TI  -)','',line)))
        # "AB  -" marks the starting line of abstract
        elif re.match('^(AB  -)',line) and not ab_ind:
            ab_ind = True
            ab_tokens.extend(nltk.word_tokenize(re.sub('(AB  -)','',line)))
        elif ab_ind and re.match('\s{6}',line):
            ab_tokens.extend(nltk.word_tokenize(re.sub('(AB  -)','',line)))
        # a new section immediately after AB will not start with 6 white spaces
        elif ab_ind and not re.match('\s{6}',line):
            # text cleaning
            pmid_ab[pmid] =  clean_text(ab_tokens)
            ab_ind = False
        else:
            continue

abspath_writeto = re.sub('.txt','.json',abspath_fn)
with open(abspath_writeto,'w') as fw:
    json.dump(pmid_ab, fw, indent=4)







