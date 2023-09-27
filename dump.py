# from typing import List, Type, Tuple, Union

# class func:
#     def _parse(text: str) -> List[str]:
#         nlp = spacy.load("en_core_web_sm")
#         doc = nlp(text)
#         return [chunk.text for chunk in doc.noun_chunks]

# print(func._parse("This is an apple."))

# import spacy
# import pyate

# nlp = spacy.load('en_core_web_sm') nlp.add_pipe("combo_basic") # or any of `basic`, `weirdness`, `term_extractor`
# or `cvalue` # source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1994795/ string = 'Central to the development of
# cancer are genetic changes that endow these “cancer cells” with many of the hallmarks of cancer,
# such as self-sufficient growth and resistance to anti-growth and pro-death signals. However, while the genetic
# changes that occur within cancer cells themselves, such as activated oncogenes or dysfunctional tumor suppressors,
# are responsible for many aspects of cancer development, they are not sufficient. Tumor promotion and progression
# are dependent on ancillary processes provided by cells of the tumor environment but that are not necessarily
# cancerous themselves. Inflammation has long been associated with the development of cancer. This review will
# discuss the reflexive relationship between cancer and inflammation with particular focus on how considering the
# role of inflammation in physiologic processes such as the maintenance of tissue homeostasis and repair may provide
# a logical framework for understanding the connection between the inflammatory response and cancer.'

# doc = nlp(string)
# print(doc._.combo_basic.sort_values(ascending=False).head(5))


# import benepar, spacy
# nlp = spacy.load('en_core_web_md')
# nlp.add_pipe("benepar", config={"model": "benepar_en3"})
# doc = nlp("The Republican Party is bullshit. The Politician leading them is a phony.")
# print(doc.ents)
#
# sent = list(doc.sents)[1]  # this finds the first sentence
# print(sent._.parse_string)
# checking for the string representation of the parse tree
# (S (NP (NP (DT The) (NN time)) (PP (IN for) (NP (NN action)))) (VP (VBZ is) (ADVP (RB now))) (. .))



# doc = nlp(data)

# print("{:<15} | {:<8} | {:<15} | {:<20}".format('Token', 'Relation', 'Head', 'Children'))
# print("-" * 70)

# for token in doc:
#     print("{:<15} | {:<8} | {:<15} | {:<20}"
#           .format(str(token.text), str(token.dep_), str(token.head.text), str([child for child in token.children])))

# for reading, normalizing and exporting docs to txt
"""
# find folder dir, has list of files
path = "ohsumed-first-20000-docs/ohsumed-first-20000-docs/test/C01"
dir_list = os.listdir(path)
# print(dir_list)

# combine all txt
data = ""
for dir in dir_list:
    text_file = open(path + "/" + dir, "r")
    txt = text_file.read()
    txt = ''.join(txt.splitlines())
    data = data + txt
    text_file.close()
"""


# for openie POS tagging API (still cant run em)
"""
from openie import StanfordOpenIE

properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

with StanfordOpenIE(properties=properties) as client:
    text = 'Barack Obama was born in Hawaii. Richard Manning wrote this sentence.'
    print('Text: %s.' % text)
    for triple in client.annotate(text):
        print('|-', triple)

print('finished')
"""



# case u ever wonder how to read and write files
"""
import os

# find folder dir, has list of files
path = "ohsumed-first-20000-docs/ohsumed-first-20000-docs/test/C01"
dir_list = os.listdir(path)
# print(dir_list[0:10])

# combine all txt
data = ""
for dir in dir_list[0:10]:
    text_file = open(path + "/" + dir, "r")
    txt = text_file.read()
    txt = ''.join(txt.splitlines()).lower()
    data = data + txt + '\n'
    text_file.close()

print(data)

with open('10_files_oshumed.txt', 'w') as f:
    f.write(data)
"""


# for pushing from excel sheets to term sets
"""
# links to excel sheets
noun_link = "C:/Users/LEGION/OSHUMED_export_Noun.xlsx"
adjnoun_link = "C:/Users/LEGION/OSHUMED_export_AdjNoun.xlsx"
adjprepnoun_link = "C:/Users/LEGION/OSHUMED_export_AdjPrepNoun.xlsx"
# convert to pandas
noun_pd = pd.read_excel(noun_link)
adjnoun_pd = pd.read_excel(adjnoun_link)
adjprepnoun_pd = pd.read_excel(adjprepnoun_link)
# setify, and unionize
noun_set = set(noun_pd['Term'].unique())
adjnoun_set = set(adjnoun_pd['Term'].unique())
adjprepnoun_set = set(adjprepnoun_pd['Term'].unique())
term_set = noun_set.union(adjnoun_set, adjprepnoun_set)

with open('C01_10docs_terms.txt', 'w') as f:
    for term in term_set:
        f.write(term + '\n')
"""

