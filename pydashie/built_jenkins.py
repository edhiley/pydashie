import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests

class BuiltJenkins(DashieSampler):
    
    def name(self):
        return 'jenkinsbuilt'
            
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
	
    def sample(self):
        wikiHome = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true&tree=jobs[name,lastBuild[result]]', auth=('matthew.puzey', 'vertebrae'))
        matches= re.findall ("SUCCESS",wikiHome.text)	
        number=matches.count("SUCCESS")
        return {'number':number}
        
        