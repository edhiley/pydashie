from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime

class JiraIteration(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
    def name(self):
      return 'jiraiteration'
	#name is the link to the main.html
  
    def sample(self):
     jiraHome = requests.get("https://nhss-jira.bjss.co.uk/Dashboard.jspa", auth=('emma.holmes', 'loopyloo'), verify=False)
    #jirahome is the url where the information is
		
     announcement= '<b>(.*?)</b>'
	#Using the corresponding tags for the information you want
	
     matches = re.findall (announcement, jiraHome.text)
	#findall finds all the instances of announcement within the jiraHome
	
     iteration= matches[0]
	# brings back the first result
	
     return{
	'text':iteration,}
	#if your returning something new always make sure to include the new class ('text','value' etc)into the html or css
	