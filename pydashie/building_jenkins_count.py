import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests

class BuildingJenkinsCount(DashieSampler):
    
    def name(self):
        return 'jenkinsbuildingcount'
            
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
	
    def sample(self):
        wikiHome = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true', auth=('matthew.puzey', 'vertebrae'))
        matches= re.findall ("blue_anime",wikiHome.text)	
        number=matches.count("blue_anime")
        return {'number':number}