#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')


# In[3]:


input_df = pd.read_csv("D:\Download\Input.xlsx - Sheet1.csv")
input_df.head()


# In[ ]:


final_df = input_df


# In[146]:


raw = []


# In[147]:


for i in range(len(input_df['URL_ID'])):
    raw_request = Request(input_df['URL'][i])
    raw_request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0')
    raw_request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    resp = urlopen(raw_request)
    raw_html = resp.read()
    soup = BeautifulSoup(raw_html, 'html.parser')

    s=""
  

    for data in soup.find_all("title"):    
        sum = data.get_text()
        s+=sum

    for data in soup.find_all("p"):
        sum = data.get_text()
        s+=sum
    s1 = s
    raw.append(s)


# In[151]:


len(raw)


# In[165]:


# MasterDictionary importing
master_df = pd.read_csv("D:\Download\LoughranMcDonald_MasterDictionary_2020.csv")
# master_df.head()

neg = []
pos = []
comp = []
# As the values represent the year when they were introduced into the dictionary and -ve values indicate they were removed from the dictionary in that particular year.

# Negative numbers
for i in range(len(master_df['Negative'])):
    if master_df['Negative'][i] > 0:
        neg.append(master_df['Word'][i].lower())

# Positive numbers
for i in range(len(master_df['Positive'])):
    if master_df['Positive'][i] > 0:
        pos.append(master_df['Word'][i].lower())
            
# Complex numbers
for i in range(len(master_df['Syllables'])):
    if master_df['Syllables'][i] > 2:
        comp.append(master_df['Word'][i].lower())
            
# Finding stopwords from the data using StopWords_Generic.txt file
stopwords = []
with open('D:/Download/StopWords_Generic.txt','r') as file:
    lines = file.readlines()
    for line in lines:
        f,l = 0, len(line) # the slice you want to take
        stopwords.append(line[f:l-1].lower())


# In[166]:


c_pos = []
c_neg = []
pol = []
sub = []
avg_sen = []
per_comp = []
fog = []
avg_words = []
comp1 = []
word1 = []
syllable = []
personal_pron = []
avg_word_len = []

for s in raw:
    s1 = s
    
    import string
    string.punctuation
# Punctuation removal
    def remove_puch(text):
        text_nop = "".join([char for char in text if char not in string.punctuation])
        return text_nop
    s1 = remove_puch(s1)
    import re
# Converting the paragraph into tokens
    def tokenize(text):
        tokens = re.split('\W+',text)
        return tokens
    s1 = tokenize(s1)
# Lowercasing words to avoid case sensitivity
    def lowering(tokenized_list):
        text = [word.lower() for word in tokenized_list]
        return text
    s1 = lowering(s1)
# Removing stopwards 
    def remove_stopwords(tokenized_list):
        text = [word for word in tokenized_list if word not in stopwords]
        return text
    s1 = remove_stopwords(s1)
    

# Counting the number of respective words in our data
    count_neg = 0
    count_pos = 0
    count_comp = 0
    for i in range(len(s1)):
        if s1[i] in neg:
            count_neg = count_neg + 1
    for i in range(len(s1)):
        if s1[i] in pos:
            count_pos = count_pos + 1
    for i in range(len(s1)):
        if s1[i] in comp:
            count_comp = count_comp + 1
            
    c_pos.append(count_pos)
    c_neg.append(count_neg)
    
# Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
    polarity_score = (count_pos - count_neg) / ((count_pos + count_neg) + 0.000001)
    pol.append(polarity_score)
    
# Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
    sub_score = (count_pos + count_neg) / (len(s1) + 0.000001)
    sub.append(sub_score)
    
    s2 = s

# Average Sentence Length
# Not taking punctuations into account. Only words... & only calculating sentences ending with '.' not others like '?' etc.
    avg_sen_len = len(s2.split()) / len(s2.split('.'))

# Percentage of Complex words
    Percent_comp = count_comp / len(s2.split())
    
# Fog Index
    fog_index = 0.4 * (avg_sen_len + Percent_comp)
    
    avg_sen.append(avg_sen_len)
    per_comp.append(Percent_comp)
    fog.append(fog_index)
    
# Average Number of Words Per Sentence = the total number of words / the total number of sentences
    avg_words_sentence = len(s2.split()) / len(s2.split('.'))
    avg_words.append(avg_words_sentence)
    
# Complex Word Count    
    comp_word_count = count_comp
    comp1.append(comp_word_count)
    
# Word Count = Counting the total cleaned words present in the text after removing puctuations and stopwords
    word_count = len(s1)
    word1.append(word_count)
    
# Used Porterstemmer to avoid "es", "ed" etc 
    import nltk
    ps = nltk.PorterStemmer()
    def stemming(tokenized_text):
        text = [ps.stem(word) for word in tokenized_text]
        return text
    s1 = stemming(s1)
    
# Syllable Count Per Word
    def syllable_count(word):
        word = word.lower()
        count = 0
        vowels = "aeiou"
        for index in range(0, len(word)):
            if word[index] in vowels:
                count += 1
        return count
    tot_syllable = 0
    for word in s1:
        tot_syllable = tot_syllable + syllable_count(word)
    syllable_count_per_word = tot_syllable / len(s1)
    syllable.append(syllable_count_per_word)
    
# Personal Pronouns
# \b - a word boundary (immediately on the left, there can be start of string position, or a non-word char) 
# ( - start of a capturing group with ID 1: I|we|my|ours - one of the I, we, my, ours words | 
#  - or (?-i:us) - inline modifier group where matching is CASE SENSITIVE, and this only matches us (not US) ) 
# - end of the group \b - as the previous char was a word char, the next position is either end of string, 
# or there is a non-word char following.
    import re
    pronounRegex = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
    s3 = s
    # for case where I'm or we're
    s3 = s3.replace("'"," ")
    personal_pronoun = len(pronounRegex.findall(s3))
    personal_pron.append(personal_pronoun)
    
# Average Word Length (Punctuations are removed to avoid unnecessary char length)
    s4 = s
    s4 = remove_puch(s4)
    s4 = tokenize(s4)
    char_len = 0
    for word in s4:
        char_len = char_len + len(word)
    avg_wordlen = char_len / len(s4)
    avg_word_len.append(avg_wordlen)


# In[167]:


final_df['POSITIVE SCORE'] = c_pos
final_df['NEGATIVE SCORE'] = c_neg
final_df['POLARITY SCORE'] = pol
final_df['SUBJECTIVITY SCORE'] = sub
final_df['AVG SENTENCE LENGTH'] = avg_sen
final_df['PERCENTAGE OF COMPLEX WORDS'] = per_comp
final_df['FOG INDEX'] = fog
final_df['AVG NUMBER OF WORDS PER SENTENCE'] = avg_words
final_df['COMPLEX WORD COUNT'] = comp1
final_df['WORD COUNT'] = word1
final_df['SYLLABLE PER WORD'] = syllable
final_df['PERSONAL PRONOUNS'] = personal_pron
final_df['AVG WORD LENGTH'] = avg_word_len

final_df.head()


# In[169]:


final_df.to_csv('D:\Download\output.csv')


# In[ ]:




