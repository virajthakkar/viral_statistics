import data_sourcing
import task

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


disease_name="covid"
synonyms=['incubation','incubate']
addons=['days', 'time','period','time period']
ner_list=['DATE','TIME']
incubation=task.Task(synonyms,addons,ner_list)
recovery=task.Task(['recovery','recovered','cured'],addons,ner_list)
survival=task.Task(['survival','survive','survives'],addons,ner_list)
death=task.Task(['death','case fatality','mortality'],['rate','percent','risk','ratio'],['PERCENT'])


pubmed=data_sourcing.PubMed() 
cambridge=data_sourcing.Cambridge()

tasks=[incubation,recovery]#  ,survival,death]
#tasks=[death]
sources=[pubmed,cambridge]
# disease=input()

data={}  #dictionary of data , key= task name, value= dic with keys as source names e.g. data['incubation']--->  {dic_from_pubmed, dic_from_google } 
for task in tasks:
    task_name=task.get_synonyms()[0].strip()  #e.g. incubation, recovery etc
    data[task_name]={}  #add dic to this list from various sources
    for source in sources:
        data[task_name][source.get_source_name()]=source.search(disease_name,task)
        #data[task_name].append(source.search(disease_name,task))


# print(incubation.get_synonyms())
# print(incubation.get_addons())

task_list_names=list(data.keys())
print(task_list_names)

source_list_names=[s.get_source_name() for s in sources]

for task_name in task_list_names:
    print("*************************************************** ",task_name,"  ***********************************************************************************************************************************")
    for source_name in source_list_names:
        print("----------------------------------------SOURCE: ",source_name,"--------------------------------------------------------------------------")

        dic=data[task_name][source_name]
        


        ct=0
        for k in list(dic.keys()):
            if len(dic[k]['sentences'])>0:
                ct+=1
                print("------------------------------------------- ",ct," ----------------------------------------------------------")
                print(k)
                print("Title: ", dic[k]['title'])
                print("-----------------------------------------------------------------------------------------------------")
                print(dic[k]['sentences'])
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print('\n')


        print("From {}, Total articles for task {}: ".format(source_name,task_name), ct)

print("*******************************************************************END OF PROGRAM********************************************************************")

