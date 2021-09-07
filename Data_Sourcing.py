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

    def search(self,disease,task):
        disease_name=disease
        synonyms=task.get_synonyms()
        addons=task.get_addons()
        nlp = spacy.load("en_core_web_sm")
        filter_words=synonyms

        
        def search_given_str(this_str,filter_words,dic={},no_articles=20,base_url="https://pubmed.ncbi.nlm.nih.gov/"):
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

            def sentences(text):
                text=re.split("(?<!\d)[.?](?!\d)\s*", text)  # . not between numbers (negative lookbehind)
                clean_sent = []
                for sent in text:
                    if sent!='':
                        clean_sent.append(sent.strip())
                return clean_sent
            
            def filter_sent_from_list(sents, filter_words):
                filter_words=[s.lower().strip() for s in filter_words]
                sent_list=[]
                for s in sents:
                    set_s=set(s.lower().split())
                    set_filter_words=set(filter_words)
                    if (set_s & set_filter_words):
                        doc=nlp(s)
                        c=0
                        for ent in filter(lambda e: e.label_=='DATE',doc.ents):
                            c+=1

                        if (c>0):
                            sent_list.append(s)
                        else:
                            pass
                    else:
                        pass
                return sent_list

            def abs_to_sent(abstract):  #Returns list of filtered sentences from the abstract
                sents=sentences(abstract)
                sent_list=filter_sent_from_list(sents, filter_words)
                return sent_list
                

            for i in range(len(abs_list)):
                sentences_list.append(abs_to_sent(abs_list[i]))

            for i in range(len(pmid_list)):
                article_dic={}
                article_dic['title']=title_list[i]
                article_dic['abstract']=abs_list[i]
                article_dic['sentences']=sentences_list[i]
                article_dic['citations']=citations_list[i]
                dic[pmid_list[i]]=article_dic
            return dic

        def give_str(disease_name,s_list,a_list):
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

        list_strings_to_search=give_str(disease_name,synonyms,addons)

        dic={}
        for l in tqdm(list_strings_to_search):
            print(l)
            dic=search_given_str(l,synonyms,dic)

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