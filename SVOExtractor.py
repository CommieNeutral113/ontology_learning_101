from openie import StanfordOpenIE
import pandas as pd

# https://stanfordnlp.github.io/CoreNLP/openie.html#api
# Default value of openie.affinity_probability_cap was 1/3.
properties = {
    'openie.affinity_probability_cap': 1/8,
}

path = "small_teddy.txt"
txt = open(path, 'r').read()
txt = ' '.join(txt.splitlines())


with StanfordOpenIE(properties=properties) as client:
    # print('Text: %s.' % text)
    # for triple in client.annotate(text):
    #     print('|-', triple)
    result = client.annotate(txt)
    df = pd.DataFrame.from_dict(result)
    df.to_excel('small_teddy_SVO1.xlsx')
    print('Finished')




"""
data = pd.read_excel('small_teddy_SVO.xlsx')
data = data[['subject', 'relation', 'object']]
data = data.sort_values(by=['subject', 'relation'])
data = data.reset_index(drop= True)

# sample code: clearing objects, clearing relations in dump.py
# object filtering
ind = 0
delete_lst = []

while (ind < len(data.index) - 5): # bừa, again
    match_lst = []
    while (len(match_lst) == 0 or
        (data.iloc[ind].loc['subject'] == data.iloc[ind - 1].loc['subject'] 
        and data.iloc[ind].loc['relation'] == data.iloc[ind - 1].loc['relation'])): # cant get the logic down
        match_lst.append(ind)
        ind += 1

    for i in range(len(match_lst)):
        for j in range(i + 1, len(match_lst)):
            str_i_set = set(data.iloc[match_lst[i]].loc['object'].split(' '))
            str_j_set = set(data.iloc[match_lst[j]].loc['object'].split(' '))
            if (str_i_set.issubset(str_j_set)):
                if (match_lst[i] not in delete_lst):
                    delete_lst.append(match_lst[i])
            elif (str_j_set.issubset(str_i_set)):
                if (match_lst[j] not in delete_lst):
                    delete_lst.append(match_lst[j])

print(delete_lst)

new_data = data.drop(index=delete_lst).reset_index(drop= True)
print(new_data)

#dòng sau có thể sai
new_data.to_excel('small_teddy_SVO1.xlsx')

"""



"""
data = pd.read_excel('small_teddy_SVO1.xlsx')
data = data[['subject', 'relation', 'object']]
data = data.sort_values(by=['subject', 'object'])
data = data.reset_index(drop= True)
# relation filtering
ind = 0
delete_lst = []

while (ind < len(data.index) - 5): # chọn bừa
    match_lst = []
    while (len(match_lst) == 0 or
        (data.iloc[ind].loc['subject'] == data.iloc[ind - 1].loc['subject'] 
        and data.iloc[ind].loc['object'] == data.iloc[ind - 1].loc['object'])): # cant get the logic down
        match_lst.append(ind)
        ind += 1

    for i in range(len(match_lst)):
        for j in range(i + 1, len(match_lst)):
            str_i_set = set(data.iloc[match_lst[i]].loc['relation'].split(' '))
            str_j_set = set(data.iloc[match_lst[j]].loc['relation'].split(' '))
            if (str_i_set.issubset(str_j_set)):
                if (match_lst[i] not in delete_lst):
                    delete_lst.append(match_lst[i])
            elif (str_j_set.issubset(str_i_set)):
                if (match_lst[j] not in delete_lst):
                    delete_lst.append(match_lst[j])

print(delete_lst)

new_data = data.drop(index=delete_lst).reset_index(drop= True)
print(new_data)

#dòng sau có thể sai
new_data.to_excel('small_teddy_SVO2.xlsx')
"""