# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12RTOR7hvwIKFfABMiK4JySPJsLim3sDZ
"""

#importing library
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import numpy as np
from google.colab import files
import nltk
import string
nltk.download('punkt')

from google.colab import drive
drive.mount('/content/drive')

df  = pd.read_excel("/content/drive/MyDrive/20211030 Test Assignment/Input.xlsx")

df

print(df['URL'][0])

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}#giving user access
 def urltotext(url):
    paragraphs=[]
    data = requests.get(url,headers=headers).text
    soup = BeautifulSoup(data,'lxml')
    title=soup.findAll(attrs={'class':'entry-title'})#extracting title of website
    title=title[0].text.replace('\n',"  ").replace('/',"")
    p=soup.find_all('p')
    for paragraph in p:
        paragraph=paragraph.text.strip()
        paragraphs.append(paragraph)
    text=''.join(paragraphs)
    text=title+" "+text
    return text
df['text']=df['URL'].apply(urltotext)

for i in df.index:
    filename=str(df['URL_ID'][i])
    text=str(df['text'][i])
    path='articles/'+filename+'.txt'

    if not os.path.exists(path):
        text_file = open(path,'w',encoding='utf-8')
        text_file.write(text)
        text_file.close()

import os

# Create directory if it doesn't exist
directory = 'articles/'
if not os.path.exists(directory):
    os.makedirs(directory)

# Your existing code
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}#giving user access
def urltotext(url):
    paragraphs=[]
    data = requests.get(url,headers=headers).text
    soup = BeautifulSoup(data,'lxml')
    title=soup.findAll(attrs={'class':'entry-title'})#extracting title of website
    title=title[0].text.replace('\n',"  ").replace('/',"")
    p=soup.find_all('p')
    for paragraph in p:
        paragraph=paragraph.text.strip()
        paragraphs.append(paragraph)
    text=''.join(paragraphs)
    text=title+" "+text
    return text

df['text']=df['URL'].apply(urltotext)

# Writing data to files
for i in df.index:
    filename = str(df['URL_ID'][i])
    text = str(df['text'][i])
    path = directory + filename + '.txt'

    # Open file and write text
    with open(path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

with open('/content/drive/MyDrive/20211030 Test Assignment/MasterDictionary/positive-words.txt','r') as f:
    positivewords=f.read()

positive_words=positivewords.split('\n')

positive_words

with open('/content/drive/MyDrive/20211030 Test Assignment/MasterDictionary/negative-words.txt', 'r', encoding='latin-1') as f1:
    negativewords = f1.read()

negative_words=negativewords.split('\n')
negative_words

stop_words=[]
with open("/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_Auditor.txt",'r') as f:
    stopwordsauditor=f.read()
    stop_words_auditor=(stopwordsauditor.split('\n'))
stop_words_auditor

with open('/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_Generic.txt','r') as f:
    stopwordsgeneric=f.read()
    stop_words_generic=stopwordsgeneric.split('\n')
with open('/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_GenericLong.txt','r') as f:
    stopwordsgenericlong=f.read()
    stop_words_generic_long=stopwordsgeneric.split('\n')
with open('/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_Currencies.txt','r', encoding='latin-1') as f:
    stopwordscurrencies=f.read()
    stop_words_currencies_=stopwordscurrencies.split('\n')

stop_words_currencies=[]
for i in stop_words_currencies_:
    stop_words_currencies.append(i.split('|')[0].strip())

with open("/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_DatesandNumbers.txt",'r') as f:
    stopwordsdateandnumbers=f.read()
    stop_words_datendnumbers_=stopwordsdateandnumbers.split('\n')

stop_words_dateandnumbers=[]
for i in stop_words_datendnumbers_:
    if "|" in i:
           stop_words_dateandnumbers.append(i.split('|')[0].strip())
    else:
        stop_words_dateandnumbers.append(i)

with open("/content/drive/MyDrive/20211030 Test Assignment/StopWords/StopWords_Geographic.txt",'r') as f:
    stopwordsgeographic=f.read()
    stop_words_geographic_=stopwordsgeographic.split('\n')

stop_words_geographic=[]
for i in stop_words_geographic_:
    if "|" in i:
           stop_words_geographic.append(i.split('|')[0].strip())
    else:
        stop_words_geographic.append(i)

stop_words_geographic

stop_words=stop_words_geographic+stop_words_dateandnumbers+stop_words_currencies+stop_words_generic_long+stop_words_generic+stop_words_auditor
stop_words

def positive_score(text):
    score=0
    for i in text.split():
        if i.upper() in stop_words:#since all values in stop_words are in upper case
            continue
        if i.lower() in positive_words: #since all values in positive_words list are in lower case
            score+=1
    return score

df['POSITIVE SCORE']=df.text.apply(positive_score)

df

def negative_score(text):
    score=0

    for i in text.split():
        if i.upper() in stop_words:#since all values in stop_words are in upper case
            continue
        if i.lower() in negative_words: #since all values in negative_words list are in lower case
            score+=1
    return score

df['NEGATIVE SCORE']=df.text.apply(negative_score)

df['POLARITY SCORE']=(df['POSITIVE SCORE']-df['NEGATIVE SCORE'])/(df['POSITIVE SCORE']+df['NEGATIVE SCORE']+(0.00001))

#For this operation we need to first calculate Total Words after cleaning
def total_words_after_cleaning(text):
    score=0
    for i in text.split():
        if i.upper() in stop_words:#since all values in stop_words are in upper case
            continue
        score+=1

    return score
df['WORD COUNT']=df.text.apply(total_words_after_cleaning)
df['SUBJECTIVITY SCORE']=(df['POSITIVE SCORE']+df['NEGATIVE SCORE'])/(df['WORD COUNT']+0.000001)

import math
def avsentlen(text):
    asl=len(text.split())/len(text.split("."))
    return math.floor(asl)

df['AVERAGE SENTENCE LENGTH']=df.text.apply(avsentlen)

#Program to find no of syllable
def syllable_count(word):
    sc=0
    for w in word:
        if(w=='a' or w=='e' or w=='i' or w=='o' or w=='u' or w=='A' or w=='E' or w=='I' or w=='O' or w=='U'):
            sc+=1
    if word[-2:]=='es' and  word[-2:]=='ES' and  word[-2:]=='ed' and  word[-2:]=='ED':
        sc=sc-2
    return sc

#Program to find complex word count
def complex_word_count(text):
    complex_word_count=0
    for word in text.split(" "):
        sc=syllable_count(word)
        if sc>=2:
            complex_word_count+=1
    return complex_word_count


df['COMPLEX_WORD_COUNT']=df.text.apply(complex_word_count)
df['PERCENTAGE OF COMPLEX WORDS']=(df['COMPLEX_WORD_COUNT']/df['WORD COUNT'])*100

df

##Program to find syllable per word
def syllable_count_perword(text):
    syllable_count_list=[]
    for word in text.split(' '):
        if word in stop_words:
            continue
        else:
            sc=syllable_count(word)
            syllable_count_list.append(sc)

    scpw=np.mean(syllable_count_list)
    return scpw
df['AVERAGE SYLLABLE COUNT PER WORD']=df.text.apply(syllable_count_perword)

perpronoun=['I',"we","my","ours","us"]

#function for personal pronoun count
def perpronoun_count(text):
    pprc=0
    for word in text.split(' '):
        if word.lower() in perpronoun or word in perpronoun:#there's no such word as 'i' in Modern English.
            if word=='US':
                continue
            else:
                pprc+=1
    return pprc

df['PERSONAL PRONOUNS']=df.text.apply(perpronoun_count)
df

##function for word Length Average Word Length
def wordlengthaverage(text):
    word_len=[]
    for word in text.split(' '):
        word_len.append(len(word))
    wla=np.mean(word_len)
    return wla

df['AVG WORD LENGTH']=df.text.apply(wordlengthaverage)
df['FOG INDEX']=0.4*(df['AVERAGE SENTENCE LENGTH']+df['PERCENTAGE OF COMPLEX WORDS'])
#Since Average Number of Words Per Sentence and AVERAGE SENTENCE LENGTH has the same formula
df['AVG NUMBER OF WORDS PER SENTENCE']=df['AVERAGE SENTENCE LENGTH']
df.columns

output_df=df.drop(['text'],axis=1)

output_df.columns

outputex=pd.read_excel('/content/drive/MyDrive/20211030 Test Assignment/Output Data Structure.xlsx') #loading output structure to match current op file
#columns

outputex.columns

output_df__formatted=output_df[['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
       'SUBJECTIVITY SCORE', 'AVERAGE SENTENCE LENGTH',
       'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
       'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX_WORD_COUNT', 'WORD COUNT',
       'AVERAGE SYLLABLE COUNT PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']]
output_df__formatted.columns=['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
       'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
       'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
       'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
       'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH']
output_df__formatted

filename = 'OutputData.xlsx'
# saving the excel
output_df__formatted.to_excel(filename)

