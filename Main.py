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
addons=[' days', ' time',' period',' time period ']

incubation=task.Task(synonyms,addons)
recovery=task.Task(['recovery','recovered','cured'],addons)
survival=task.Task(['survival','survive','survives'],addons)
#carrier_period=Task('carrier',['recovered','cured'],['days','time','period','hours'])


pb=data_sourcing.PubMed() 

tasks=[incubation,recovery,survival]
sources=[pb]
# disease=input()

data={}  #dictionary of data , key= task name, value= list from sources e.g. data['incubation']---> [ dic_from_pubmed, dic_from_google  ]
for task in tasks:
    task_name=task.get_synonyms()[0].strip()  #e.g. incubation, recovery etc
    data[task_name]=[]  #add dic to this list from various sources
    for source in sources:
        data[task_name].append(source.search(disease_name,task))


# print(incubation.get_synonyms())
# print(incubation.get_addons())

task_list_names=list(data.keys())
print(task_list_names)

for task_name in task_list_names:
    dic=data[task_name][0]
    print("*************************************************** ",task_name,"  ***********************************************************************************************************************************")


    ct=0
    for k in list(dic.keys()):
        if len(dic[k]['sentences'])>0:
            ct+=1
            print("------------------------------------------- ",ct," ----------------------------------------------------------")
            print(k)
            print("Title: ", dic[k]['title'])
            print("-----------------------------------------------------------------------------------------------------")
            print(dic[k]['sentences'], dic[k]['citations'])
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print('\n')


    print("Total articles for task {}: ".format(task_name), ct)

print("*******************************************************************END OF PROGRAM********************************************************************")

