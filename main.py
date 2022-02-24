# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 23:11:28 2022

@author: William J. Wakefield
@author: CJ Bauer

The system should:
o Create the inverted index (the dictionary and postings lists) for your collection of documents
o Parse and execute simple queries
o Perform simple tokenization and normalization of the text such as removing digits, punctuation
marks, etc.
o Statistics:
1) Report the number of distinct words observed in each document, and the total number of
words encountered.
2) Report the number of distinct words observed in the whole collection of documents, and the
total number of words encountered.
3) Report the total number of times each word is seen (term frequency) and the document IDs
where the word occurs (Output the posting list for a term).
4) Report the top 100th, 500th, and 1000th most-frequent word and their frequencies of
occurrence.
5) Create postings and assign a term frequency to every document in postings list.
6) Provide a simple GUI to test the system.
"""
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import sent_tokenize , word_tokenize
import glob
import re
import os
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QTextEdit, QPushButton
from PyQt5 import uic
import sys

Stopwords = set(stopwords.words('english'))


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        #Load UI file
        uic.loadUi("IRSystem.ui", self)
        
        #Show the app
        self.show()
    
    
#initialize app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
def finding_all_unique_words_and_freq(words):
    words_unique = []
    word_freq = {}
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq

def finding_freq_of_word_in_doc(word,words):
    freq = words.count(word)
        
def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex,'',text)
    return text_returned

class Node:
    def __init__(self ,docId, freq = None):
        self.freq = freq
        self.doc = docId
        self.nextval = None
    
class SlinkedList:
    def __init__(self ,head = None):
        self.head = head
        
 #find unique words from each doc in the dataset       
all_words = []
dict_global = {}
file_folder = 'data/*'

idx = 1
files_with_index = {}
for file in glob.glob(file_folder):
    print(file)
    fname = file
    file = open(file , "r")
    text = file.read()
    text = remove_special_characters(text) 
    text = re.sub(re.compile('\d'),'',text)
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    dict_global.update(finding_all_unique_words_and_freq(words))
    files_with_index[idx] = os.path.basename(fname)
    idx = idx + 1
    
unique_words_all = set(dict_global.keys())

        
linked_list_data = {}
for word in unique_words_all:
    linked_list_data[word] = SlinkedList()
    linked_list_data[word].head = Node(1,Node)
    
word_freq_in_doc = {}
idx = 1

for file in glob.glob(file_folder):
    file = open(file, "r")
    text = file.read()
    text = remove_special_characters(text)
    text = re.sub(re.compile('\d'),'',text)
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    word_freq_in_doc = finding_all_unique_words_and_freq(words)

    for word in word_freq_in_doc.keys():
        linked_list = linked_list_data[word].head
        while linked_list.nextval is not None:
            linked_list = linked_list.nextval
        linked_list.nextval = Node(idx ,word_freq_in_doc[word])
    idx = idx + 1
    
query = input('Enter your query:')
query = word_tokenize(query) #tokenize provided by NLTK

connecting_words = []
cnt = 1

different_words = []

for word in query:
    if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
        different_words.append(word.lower())
    else:
        connecting_words.append(word.lower())
        
print("Connecting Words: \n", connecting_words)
total_files = len(files_with_index)

zeroes_and_ones = []
zeroes_and_ones_of_all_words = []
for word in (different_words):
    if word.lower() in unique_words_all:
        zeroes_and_ones = [0] * total_files
        linkedlist = linked_list_data[word].head
        print("word: ", word)
        while linkedlist.nextval is not None:
            zeroes_and_ones[linkedlist.nextval.doc - 1] = 1
            linkedlist = linkedlist.nextval
        zeroes_and_ones_of_all_words.append(zeroes_and_ones)
    else:
        print(word," not found")
        sys.exit()
        

for word in connecting_words:
    word_list1 = zeroes_and_ones_of_all_words[0]
    word_list2 = zeroes_and_ones_of_all_words[1]
    if word == "and":
        bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,word_list2)]
        zeroes_and_ones_of_all_words.remove(word_list1)
        zeroes_and_ones_of_all_words.remove(word_list2)
        zeroes_and_ones_of_all_words.insert(0, bitwise_op);
    elif word == "or":
        bitwise_op = [w1 | w2 for (w1,w2) in zip(word_list1,word_list2)]
        zeroes_and_ones_of_all_words.remove(word_list1)
        zeroes_and_ones_of_all_words.remove(word_list2)
        zeroes_and_ones_of_all_words.insert(0, bitwise_op);
    elif word == "not":
        bitwise_op = [not w1 for w1 in word_list2]
        bitwise_op = [int(b == True) for b in bitwise_op]
        zeroes_and_ones_of_all_words.remove(word_list2)
        zeroes_and_ones_of_all_words.remove(word_list1)
        bitwise_op = [w1 & w2 for (w1,w2) in zip(word_list1,bitwise_op)]
        
        zeroes_and_ones_of_all_words.insert(0, bitwise_op);
        
files = []    
print("zeros and ones of all words in query: \n", zeroes_and_ones_of_all_words)
lis = zeroes_and_ones_of_all_words[0]
cnt = 1
for index in lis:
    if index == 1:
        files.append(files_with_index[cnt])
    cnt = cnt+1
    
print("files where query is found: \n", files)

print("number of unique words in all documents: ", len(unique_words_all))
print("Total number of words encountered: ", )