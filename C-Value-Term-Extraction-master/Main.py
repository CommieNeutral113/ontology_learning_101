import time

starttime = time.time()
from NoName import NoName

noun = ['NN', 'NNS', 'NNP', 'NNPS']  # tags of noun
adj = ['JJ']  # tags of adjective
pre = ['IN']  # tags of preposition


##Parse arguments from command line###################################################################################
def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("Data", type=str)  # input data file
    parser.add_argument("lingui_filter", type=str)
    parser.add_argument("L", type=int)  # the expected maximum length of a term
    parser.add_argument("freq_threshold", type=int)
    parser.add_argument("CValue_threshold", type=int)

    args = parser.parse_args()

    Data = args.Data
    f = open(Data).readlines()
    lingui_filter = args.lingui_filter
    L = args.L
    freq_threshold = args.freq_threshold
    CValue_threshold = args.CValue_threshold

    return f, lingui_filter, L, freq_threshold, CValue_threshold


f, lingui_filter, L, freq_threshold, CValue_threshold = parse_arguments()
"""
f = input()
lingui_filter = input()
L = int(input())
freq_threshold = int(input())
CValue_threshold = int(input())

print(f)
print(lingui_filter)
print(L)
print(freq_threshold)
print(CValue_threshold)
"""


##Extract candidate terms using different linguistic filters##################################################################################
'''
The results are saved in a dictionary named candidate, 
candidate[m] prints out a list of candidate string objects of length m
m ranges from 2 to L
'''
# init candidate list for each string's word count
candidate = candidate = dict([(key, []) for key in range(2, L + 1)])
for sentence in f:
    sentence = sentence.rstrip('\n').split(' ')
    n_words = len(sentence)
    start = 0
    while start <= n_words - 2:  # why -2? is the start redefined somewhere else?
        i = start
        noun_ind = []
        pre_ind = []
        pre_exist = False  # creating index list to find all nouns and prepositions, skip adj
        while True:
            word = NoName()
            word.word(sentence[i])  # init a word object
            if word.tag in noun:  # counting nouns
                noun_ind.append(i)
                i += 1
            elif (lingui_filter == ('AdjNoun' or 'AdjPrepNoun')) and word.tag in adj:  # checking adj
                word_next = NoName()
                word_next.word(sentence[i + 1])  # bcs adj is an indicator of nouns in short distance, we prepare a noun
                if word_next.tag in noun:
                    noun_ind.append(i + 1)
                    i += 2  # reason it's +2 instead of +1 is because we need to leave the noun behind
                elif word_next.tag in adj:
                    i += 2  # because the adj doesn't matter
                else:
                    end = i + 1
                    break  # why break here?
            elif (lingui_filter == 'AdjPrepNoun') and not pre_exist and i != 0 and (word.tag in pre):  # counting prep
                pre_ind.append(i)
                pre_exist = True
                i += 1
            else:
                end = i
                break

        if len(noun_ind) != 0:
            for i in list(set(range(start, noun_ind[-1])) - set(
                    pre_ind)):  # set is used bcs of interjection, etc. we're checking all words in perceived range, except for the prepositions
                for j in noun_ind:
                    if 1 <= j - i <= L - 1:  # that sentence[i:j + 1] makes a compound word
                        substring = NoName()
                        substring.substring(sentence[i:j + 1])
                        exist = False
                        for x in candidate[j - i + 1]:  # check for past occurences, either add to the count or init
                            if x.words == substring.words: x.f += 1; exist = True
                        if not exist:
                            candidate[j - i + 1].append(substring)
                            substring.f = 1
        start = end + 1

##Remove candidate strings with low frequency and sort them##################################################################################            
for i in range(2, L + 1):
    candidate[i] = [x for x in candidate[i] if x.f >= freq_threshold]
    candidate[i].sort(key=lambda x: x.f, reverse=True)

##Compute C-Value##################################################################################
Term = []
for l in reversed(range(2, L + 1)): # bcs CValue has an element of per-occurences, we need to consider the longer candidates first
    candi = candidate[l]
    for phrase in candi:
        if phrase.c == 0:
            phrase.CValue_non_nested()
        else:
            phrase.CValue_nested()

        if phrase.CValue >= CValue_threshold:
            Term.append(phrase)
            for j in range(2, phrase.L):
                for i in range(phrase.L - j + 1):
                    substring = phrase.words[i:i + j] # find all possible substrings of found phrase
                    for x in candidate[j]:
                        if substring == x.words:
                            x.substringInitial(phrase.f) # is this redundant??
                            for m in Term:
                                if ' '.join(x.words) in ' '.join(m.words):
                                    x.revise(m.f, m.t)

Term.sort(key=lambda x: x.CValue, reverse=True)

##Print out terms with top-10 C-Value##################################################################################           
import pandas as pd

count = 0
#ind_range = 100
result = pd.DataFrame(index=range(len(Term)), columns=['Term', 'C-Value', 'Frequency', 'Tags'])
i = 0

"""
result = pd.DataFrame(index=range(ind_range), columns=['Term', 'C-Value', 'Frequency', 'Tags'])


for x in Term[0:ind_range]:
    i += 1
    result['Term'][i] = ' '.join(x.words)
    result['C-Value'][i] = x.CValue
    result['Frequency'][i] = x.f
    result['Tags'][i] = x.tag
    if x.CValue >= CValue_threshold:
        count += 1
        

"""

while i < len(Term) and Term[i].CValue >= CValue_threshold:
    result['Term'][i] = ' '.join(Term[i].words)
    result['C-Value'][i] = Term[i].CValue
    result['Frequency'][i] = Term[i].f
    result['Tags'][i] = Term[i].tag
    count += 1
    i += 1

    # havent found a way to stop program from adding too much to the result table
print(result)

# result.to_excel('OSHUMED_export.xlsx')
if lingui_filter == 'Noun':
    result.to_excel('OSHUMED_export_Noun.xlsx')
elif lingui_filter == 'AdjNoun':
    result.to_excel('OSHUMED_export_AdjNoun.xlsx')
elif lingui_filter == 'AdjPrepNoun':
    result.to_excel('OSHUMED_export_AdjPrepNoun.xlsx')

endtime = time.time()
print('Running time: ' + str((endtime - starttime) / 60.0) + ' min')
print('A total of ' + str(count) + ' terms within range')
