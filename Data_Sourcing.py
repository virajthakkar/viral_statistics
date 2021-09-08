import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import spacy
from tqdm import tqdm
import time

from spacy.matcher import Matcher 
from spacy.matcher import PhraseMatcher
from spacy.pipeline import EntityRuler

import visualise_spacy_tree
from IPython.display import Image, display

from spacy import displacy 
import glob

from utilities import *




class Source():
    def __init__(self,source_name,base_url):
        self.__source_name=source_name
        self.__base_url=base_url

    def get_source_name(self):
        return self.__source_name

    def get_base_url(self):
        return self.__base_url

    def search(self,disease,task):
        #takes disease and task as print_default_output
        #return dictionary...
        pass


class PubMed(Source):
    def __init__(self,source_name='PubMed',base_url='https://pubmed.ncbi.nlm.nih.gov/'):
        super().__init__(source_name,base_url)


    def search_given_str(self,this_str,filter_words,ner_list,dic={},no_articles=20,base_url="https://pubmed.ncbi.nlm.nih.gov/",nlp = spacy.load("en_core_web_sm")): #reduce ident
        #"https://pubmed.ncbi.nlm.nih.gov/?term=influenza+incubation+days&filter=simsearch1.fha&format=abstract&size=20"
        search_str=base_url+ "?term="+this_str+"&filter=simsearch1.fha&format=abstract&size={}".format(no_articles)
        page = requests.get(search_str)
        soup = BeautifulSoup(page.content, 'html.parser')

        title_list=[]
        abs_list=[]
        pmid_list=[]
        citations_list=[]
        sentences_list=[]

        for i in range(no_articles):
            try:
                cur_abs=soup.find(id='search-result-1-{}-enc-abstract'.format(i+1))
                abs_list.append(cur_abs.get_text().strip())
            except:
                abs_list.append("Could not fetch the abstract")
                
            try:
                cur_title=soup.find(id='search-result-1-{}-short-view-heading'.format(i+1))
                title_list.append(cur_title.find(class_='heading-title').get_text().strip() )
            except:
                title_list.append("Could not fetch the title")

            try:
                cur_pmid=soup.find(id='search-result-1-{}-full-view-identifiers'.format(i+1))
                pid=cur_pmid.find(class_='current-id').get_text().replace(" ","")
                pmid_list.append(pid)
            except:
                pmid_list.append("0")

            
        for pi in range(len(pmid_list)):
            
            try:
                r1=soup.find('a', href = re.compile(r'/{}/#citedby'.format(pmid_list[pi]))).get_text().strip().replace(" ","").replace('\n','')
                ct=re.findall(r'\d+',r1)
                citations_list.append(int(ct[0]))
            except:
                citations_list.append(0)


        for i in range(len(abs_list)):
            sentences_list.append(abstract_to_relevant_sentences(abs_list[i],filter_words,ner_list,nlp))

        for i in range(len(pmid_list)):
            article_dic={}
            article_dic['title']=title_list[i]
            article_dic['abstract']=abs_list[i]
            article_dic['sentences']=sentences_list[i]
            article_dic['citations']=citations_list[i]
            dic[pmid_list[i]]=article_dic
        return dic




    def search(self,disease,task):
        disease_name=disease
        synonyms=task.get_synonyms()
        addons=task.get_addons()
        ner_list=task.get_ner()
        nlp = spacy.load("en_core_web_sm")
        filter_words=synonyms

    
        list_strings_to_search=give_str(disease_name,synonyms,addons)

        dic={}
        for l in tqdm(list_strings_to_search):
            print(l)
            dic=self.search_given_str(l,filter_words,ner_list,dic)

        return dic



# class Google_Search(Source):
#     def __init__(self):
#         super().__init__('PubMed','https://google.com/')
        
#     def search(self,disease,task):
#         return dic

# class Custom_source(Source):
#     def __init__(self):
#         super().__init__('Some_name','https://somewebsite.com/')

#     def search(self,disease,task):
#         return dic