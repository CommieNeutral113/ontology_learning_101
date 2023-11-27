from coref_stage import Coref
from TermsExtractor import extractor
from NER import FlairNER, SpacyNER
from nltk import StanfordPOSTagger, word_tokenize, sent_tokenize
from openie import StanfordOpenIE
import pandas as pd
import os

# Your java path
# Dont know where? just google it
os.environ["JAVAHOME"] = "C:/Program Files/Java/jre1.8.0_361/bin/java.exe"

JAR = 'C-Value-Term-Extraction-master/stanford-postagger-2017-06-09/stanford-postagger-2017-06-09/stanford-postagger.jar'
TAG_MODEL = 'C-Value-Term-Extraction-master/stanford-postagger-2017-06-09/stanford-postagger-2017-06-09/models/english-bidirectional-distsim.tagger'

TAGGER = StanfordPOSTagger(TAG_MODEL, JAR, encoding = "utf-8")

current_dir = os.getcwd().replace('\\', '/')
wiki_dir_path = current_dir + '/Wiki_dataset'
wiki_dir_list = dir_list = os.listdir(wiki_dir_path)

file_name_list = []
for file in wiki_dir_list:
    file_name_list.append(file.split('.txt')[0])

# for name in file_name_list:

new_txt = Coref('Wiki_dataset/Warren Buffet.txt')

print('new text: ', new_txt)
with open('new_text.txt', 'w') as file:
    for line in new_txt:
        line = line.strip()
        if (line[-1] != '.'):
            line += '.'
        file.write(line + '\n')
    file.close()


properties = {
    'openie.affinity_probability_cap': 1/10,
}

path = "new_text.txt"
txt = open(path, 'r').read()
txt = ' '.join(txt.splitlines())

# print(txt)

with StanfordOpenIE(properties=properties) as client:
    result = client.annotate(txt)
    # print(result)
    df = pd.DataFrame.from_dict(result)
    # graph_image = 'graph.png'
    # client.generate_graphviz_graph(txt, graph_image)
    # print('Graph generated: %s.' % graph_image)

    print('Finished relation extraction\n')

# list các câu sau khi được coref
sentences = []

with open('new_text.txt', 'r') as file:
    line = file.readline()
    while (line != ''):
        line = line.strip('\n')
        print('line in new text:', line)
        sentences.append(line)

        line = file.readline()
    
    sentencesTokenized = [word_tokenize(sentence) for sentence in sentences]
    # print(sentencesTokenized)

    file.close()

tagged_sentences = TAGGER.tag_sents(sentencesTokenized)
# print(tagged_sentences)

tagged_text = ''
for tagged_sentence in tagged_sentences:
    tagged_words = []
    for word, tag in tagged_sentence:
        tagged_words.append(f"{word}_{tag}")
    tagged_sentence_str = " ".join(tagged_words)
    tagged_text += tagged_sentence_str + ' '

tagged_text = [tagged_text]

term_list1 = extractor(tagged_text, 'Noun', 8, 2, 1)
term_list2 = extractor(tagged_text, 'AdjNoun', 8, 2, 1)
term_list3 = extractor(tagged_text, 'AdjPrepNoun', 8, 2, 1)

final_term_list = pd.concat([term_list1, term_list2, term_list3], ignore_index=True).drop_duplicates(subset='Term')
# print(final_term_list)

final_term_list.to_excel('OSHUMED_terms.xlsx')


ner_df = SpacyNER(sentences)

ner_df = ner_df.loc[(ner_df['Label'] == 'PERSON') |
                    (ner_df['Label'] == 'FAC') |
                    (ner_df['Label'] == 'NORP') |
                    (ner_df['Label'] == 'GPE') |
                    (ner_df['Label'] == 'LOC') |
                    (ner_df['Label'] == 'ORG')]


terms = final_term_list['Term'].values.tolist()
terms += ner_df['Entity'].values.tolist()
print(terms)

filtered_rows = []
for i in range(len(df.index)):
    for term in terms:
        row = df.iloc[i]
        if ((term in row['subject']) and (term in row['object'])):
            # print(row)
            filtered_rows.append(row)
            break

final_relation = pd.DataFrame(filtered_rows)

print(final_relation)

final_relation.to_excel('OSHUMED_SVO.xlsx')

# ner_df = ner_df.loc[(ner_df['Label'] == ('PERSON' or 'FAC' or 'NORP' or 'GPE' or 'LOC' or 'ORG'))]

ner_df.to_excel('Ner_xlsx/Oshumed_NER.xlsx')

