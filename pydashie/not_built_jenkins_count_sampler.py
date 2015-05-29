import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests

class FailJenkinsCount(DashieSampler):
    
    def name(self):
        return 'jenkinsfailedcount'
            
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
	
    def sample(self):
        wikiHome = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true&tree=jobs[name,lastBuild[result]]', auth=('matthew.puzey', 'vertebrae'))
        matches= re.findall ("FAILURE",wikiHome.text)	
        number=matches.count("FAILURE")
		
        wikiHome2 = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true' , auth=('matthew.puzey', 'vertebrae'))
        matches= re.findall ("red_anime",wikiHome2.text)
        fail=matches.count("red_anime")
		
        total= fail+number
        return {'number':total}
        
 #PUT IN FAILED IN PROCESS       