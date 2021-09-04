class Source():
    def __init__(self,name,base_url):
        self.name=name
        self.base_url=base_url

    def search(self,disease,task):
        #takes disease and task as print_default_output
        #return dictionary of sentences...
        pass


class PubMed(Source):
    def __init__(self):
        super().__init__('PubMed','https://pubmed.ncbi.nlm.nih.gov/')

    def search(self,disease,task):
        #...
        return None



class Google_Search(Source):
    def __init__(self):
        super().__init__('PubMed','https://google.com/')


class custome_scource
