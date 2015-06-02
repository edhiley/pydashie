import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests

class JenkinsBuildingCount(DashieSampler):
    
    def name(self):
        return 'jenkinsbuildingcount'
	#name is the link to the main.html
            
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
	
    def sample(self):
        wikiHome = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true', auth=('matthew.puzey', 'vertebrae'))
        #wikihome is the api address where the information is
		
        matches= re.findall ("blue_anime",wikiHome.text)	
		#findall returns all the times the result you want is in the api
        		
        number=matches.count("blue_anime")
		#this counts the number of results
		
		
        return {'number':number}
			#if your returning something new always make sure to include the new class ('number' etc)into the html or css