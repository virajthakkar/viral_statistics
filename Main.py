import Data_Sourcing
import Task


incubation_period=Task('incubation',['incubate','incubation'],['day','time','period','hours'])
recovery_period=Task('recovery',['recovered','cured'],['day','time','period','hours'])
carrier_period=Task('carrier',['recovered','cured'],['day','time','period','hours'])

tasks=[incubation_period,recovery_period,carrier]
sources=[PubMed(),Google_Search()]
disease=input()

data={}
for task in tasks:
    data[task.name]=[]
    for source in sources:
        data[task.name].append(source.search(disease,task))
