
#Incubation period
#Recovery period
#Case Fatality Rate

class Task():
    def __init__(self,synonyms=[],addons=[]):
        #self.__name=name
        self.__synonyms=synonyms #list of names of task e.g ['Incubation','Incubate'] e.g ['recovery','recovered']
        self.__addons=addons  # list of search words e.g. ['days','time','period','time period']

    def add_synonyms(self,value):
        self.__synonyms.append(value)

    def add_addons(self,value):
        self.__addons.append(value)

    
    def set_synonyms(self, synonyms_list):
        self.__synonyms=synonyms_list

    def set_addons(self, addons_list):
        self.__addons=addons_list

   
    def get_synonyms(self):
        return self.__synonyms

    def get_addons(self):
        return self.__addons



