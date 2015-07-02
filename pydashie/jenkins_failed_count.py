import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests

class JenkinsFailedCount(DashieSampler):
    
    def name(self):
        return 'jenkinsfailedcount'
    #name is the link to the main.html        
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
	
    def sample(self):
        wikiHome = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true&tree=jobs[name,lastBuild[result]]', auth=('emma.holmes11', 'vertebrae'))
        wikiHome2 = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true' , auth=('emma.holmes11', 'vertebrae'))
		#wikihome and wikihome2 are the api address' where the information is
		
        matchesfail= re.findall ("FAILURE",wikiHome.text)	
        matchesfailinprocess= re.findall ("red_anime",wikiHome2.text)
        #findall returns all the times the result you want is in the api

        fail=matchesfail.count("FAILURE")     
        failinprocess=matchesfailinprocess.count("red_anime")
		#this counts the number of results
		
        total= fail+failinprocess
		#this added the counts together
		
		
        return {'number':total}
		#if your returning something new always make sure to include the new class ('number' etc)into the html or css
        
     