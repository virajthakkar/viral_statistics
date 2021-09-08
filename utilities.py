
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import spacy
from tqdm import tqdm
import time

def sentences(text):  #text to sentence list
    text=re.split("(?<!\d)[.?](?!\d)\s*", text)  # . not between numbers (negative lookbehind)
    clean_sent = []
    for sent in text:
        if sent!='':
            clean_sent.append(sent.strip())
    return clean_sent



def filter_sentence_from_list(sents, filter_words,ner_list,nlp = spacy.load("en_core_web_sm")):  # input: List of sentences, output: list of filtered sentences
    filter_words=[s.lower().strip() for s in filter_words]
    sent_list=[]
    for s in sents:
        set_s=set(s.lower().split())
        set_filter_words=set(filter_words)
        if (set_s & set_filter_words):
            doc=nlp(s)

            c=len(list(filter(lambda e: e.label_ in ner_list,doc.ents)))

            if (c>0):
                sent_list.append(s)
            else:
                pass
        else:
            pass
    return sent_list


def abstract_to_relevant_sentences(abstract,filter_words,ner_list,nlp= spacy.load("en_core_web_sm")):  #Returns list of filtered sentences from the abstract
    sents=sentences(abstract)
    sent_list=filter_sentence_from_list(sents, filter_words,ner_list,nlp)
    return sent_list



def give_str(disease_name,s_list,a_list):   #gives string as word1+word2+word3
    this_str_list=[]
    disease_name=re.sub(r"\s+", '+', disease_name.strip())
    s_list=[s.lower().strip() for s in s_list]
    s_list=[re.sub(r"\s+", '+',s) for s in s_list ]
    a_list=[a.lower().strip() for a in a_list]
    a_list=[re.sub(r"\s+", '+',a) for a in a_list ]
    for s in s_list:
        for a in a_list:
            this_str_list.append(disease_name + "+"+ s+"+"+a)
    return this_str_list
