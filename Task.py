
#Incubation period
#Recovery period
#Case Fatality Rate

class Task():
    def __init__(self,name,synonyms=[],addons=[]):
        self.name=name
        self.synonyms=synonyms
        self.addons=addons

    def add_synonym(self,value):
        self.synonyms.append(value)

    def add_addon(self,value):
        self.addons.append(value)
