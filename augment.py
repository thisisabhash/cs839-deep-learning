#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: abhash
"""

import os
import re
import random
import pyiwn
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

HINDI_FULL_PATH = '/parallel/IITB.en-hi.hi'
HINDI_SUBSET_PATH = '/IITB.en-hi-100k.hi'
HINDI_RANDOM_SWAP_PATH = '/IITB.en-hi-100k-random-swap.hi'
HINDI_RANDOM_DELETE_PATH = '/IITB.en-hi-100k-random-delete.hi'
HINDI_RANDOM_INSERT_PATH = '/IITB.en-hi-100k-random-insert.hi'

ENGLISH_FULL_PATH = '/parallel/IITB.en-hi.en'
ENGLISH_SUBSET_PATH = '/IITB.en-hi-100k.en'
ENGLISH_RANDOM_SWAP_PATH = '/IITB.en-hi-100k-random-swap.en'
ENGLISH_RANDOM_DELETE_PATH = '/IITB.en-hi-100k-random-delete.en'
ENGLISH_RANDOM_INSERT_PATH = '/IITB.en-hi-100k-random-insert.en'

SIZE_SUBSET = 100000


def sanitize(line):

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ") #replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")

    return line

def sanitize_en(line):
    clean_line = ""

    line = line.replace("’", "")
    line = line.replace("'", "")
    line = line.replace("-", " ") #replace hyphens with spaces
    line = line.replace("\t", " ")
    line = line.replace("\n", " ")
    line = line.lower()

    for char in line:
        if char in 'qwertyuiopasdfghjklzxcvbnm ':
            clean_line += char
        else:
            clean_line += ' '

    clean_line = re.sub(' +',' ',clean_line) #delete extra spaces
    if clean_line[0] == ' ':
        clean_line = clean_line[1:]
    return clean_line

def random_deletion(p):

    f = open(os.getcwd()+HINDI_RANDOM_DELETE_PATH, 'w',newline='')
 
    with open(os.getcwd()+HINDI_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                
                if len(words) < 1:
                    f.write(' '+'\n')
                    continue
                
                if len(words) == 1:
                    f.write(words[0]+'\n')
                    continue
            
                new_words = []
                for word in words:
                    r = random.uniform(0, 1)
                    if r > p:
                        new_words.append(word)
            
                if len(new_words) == 0:
                    rand_int = random.randint(0, len(words)-1)
                    f.write(words[rand_int]+'\n')
                    continue

                f.write(' '.join(new_words)+'\n')
            
    f.close()
    
    f = open(os.getcwd()+ENGLISH_RANDOM_DELETE_PATH, 'w',newline='')
 
    with open(os.getcwd()+ENGLISH_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize_en(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                
                if len(words) < 1:
                    f.write(' '+'\n')
                    continue
                
                if len(words) == 1:
                    f.write(words[0]+'\n')
                    continue
            
                new_words = []
                for word in words:
                    r = random.uniform(0, 1)
                    if r > p:
                        new_words.append(word)
            
                if len(new_words) == 0:
                    #print("len: " + str(len(words)))
                    rand_int = random.randint(0, len(words)-1)
                    f.write(words[rand_int]+'\n')
                    continue

                f.write(' '.join(new_words)+'\n')
            
    f.close()

def random_swap(n):
    f = open(os.getcwd()+HINDI_RANDOM_SWAP_PATH, 'w',newline='')
 
    with open(os.getcwd()+HINDI_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                            
                for _ in range(n):
                    words = swap(words)
                
                f.write(' '.join(words)+'\n')
            
    f.close()
    
    f = open(os.getcwd()+ENGLISH_RANDOM_SWAP_PATH, 'w',newline='')
 
    with open(os.getcwd()+ENGLISH_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize_en(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                            
                for _ in range(n):
                    words = swap(words)
                
                f.write(' '.join(words)+'\n')
            
    f.close()
    
def swap(new_words):
    if len(new_words) <= 1:
        return new_words
    
    random_idx_1 = random.randint(0, len(new_words)-1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
    return new_words

def random_insertion(n):
    f = open(os.getcwd()+HINDI_RANDOM_INSERT_PATH, 'w',newline='')
    iwn = pyiwn.IndoWordNet()
    with open(os.getcwd()+HINDI_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                            
                new_words = words.copy()
                for _ in range(n):
                    insert_word(new_words,iwn)
                
                f.write(' '.join(words)+'\n')
            
    f.close()
    
    f = open(os.getcwd()+ENGLISH_RANDOM_INSERT_PATH, 'w',newline='')
    with open(os.getcwd()+ENGLISH_SUBSET_PATH) as file_in:
        for line in file_in:
            if len(line.strip())>0:
                sentence = sanitize_en(line.strip())
                words = sentence.split(' ')
                words = [word for word in words if word != '']
                
                new_words = words.copy()
                #print(new_words)
                for _ in range(n):
                    insert_word_en(new_words)
                
                f.write(' '.join(new_words)+'\n')
            
    f.close()
    
def insert_word(new_words, indoWordNet):
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        synonyms = get_synonyms(random_word,indoWordNet)
        counter+=1
        if counter >=10:
            return
    
    random_synonym = synonyms[0]
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)
    
def insert_word_en(new_words):
    if len(new_words) < 1:
        return
    
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        synonyms = get_synonyms_en(random_word)
        #print(synonyms)
        counter+=1
        if counter >=10:
            return
    
    random_synonym = synonyms[0]
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)

def get_synonyms(word,indoWordNet):
    synonyms = set()
    try:
        synsets = indoWordNet.synsets(word)
        if len(synsets) < 1:
            return []
    
        #print(synsets)
        for syn in synsets:
            for l in syn.lemma_names(): 
                synonym = l.replace("_", " ").replace("-", " ")
                synonyms.add(synonym) 
	
        if word in synonyms:
            synonyms.remove(word)
    
        return list(synonyms)
    except KeyError:
        return []

def get_synonyms_en(word):
	synonyms = set()
	for syn in wordnet.synsets(word): 
		for l in syn.lemmas(): 
			synonym = l.name().replace("_", " ").replace("-", " ").lower()
			synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
			synonyms.add(synonym) 
	if word in synonyms:
		synonyms.remove(word)
	return list(synonyms)

def augment():
    random_swap(1)
    random_deletion(0.1)
    random_insertion(1)

def main():
    # select a subset of data and write to a file
    if os.path.isfile(os.getcwd()+HINDI_SUBSET_PATH):
        os.remove(os.getcwd()+HINDI_SUBSET_PATH)
        
    f = open(os.getcwd()+HINDI_SUBSET_PATH, 'w',newline='')
    count = 0
    #print(os.getcwd()+HINDI_FULL_PATH)
    
    with open(os.getcwd()+HINDI_FULL_PATH) as file_in:
        for line in file_in:
            if count >= SIZE_SUBSET:
                break
            
            count+=1
            f.write(line.strip()+'\n')
            #print(line)
            
    f.close()
    
    if os.path.isfile(os.getcwd()+ENGLISH_SUBSET_PATH):
        os.remove(os.getcwd()+ENGLISH_SUBSET_PATH)
        
    f = open(os.getcwd()+ENGLISH_SUBSET_PATH, 'w',newline='')
    count = 0
    
    with open(os.getcwd()+ENGLISH_FULL_PATH) as file_in:
        for line in file_in:
            if count >= SIZE_SUBSET:
                break
            
            count+=1
            f.write(line.strip()+'\n')
            
    f.close()
            
    augment()

if __name__ == '__main__':
    main()