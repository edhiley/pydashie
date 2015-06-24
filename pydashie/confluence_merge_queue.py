from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime

class ConfluenceMergeQueue(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self): 
      return 'confluencemergequeue'
	#name is the link to the main.html
  
    def sample(self):
       wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Merge+Queue", auth=('emma.holmes', 'loopyloo'), verify=False)
	   #wikihome is the url where the information is
       match= re.findall('<div class="table-wrap"><table style="text-align: left;" class="confluenceTable"><tbody><tr>(.*?)</tr></tbody></table></div>',wikiHome.text)
       matches= re.findall ('<td colspan="1" class="confluenceTd">(.*?)</td>',str(match))
	   #Using the corresponding tags for the information you want (there weren't any specific tags so had to use "confluenceTd" which is used in all tables on the confluence page)
       
       person1=matches[0:1]
       commit1=matches[2:3]
       person2=matches[4:5]
       commit2=matches[6:7]
       person3=matches[8:9]
       commit3=matches[9:10]
	   #To get the specific result needed choose which result you need this is picking 1,5,9(if any columns are added to the table or other tables added above the result numbers wont be correct)
	   
       return {'person1': unicode(person1)[2:-2],
	           'commit1': unicode(commit1)[2:-2],
			   'person2':unicode(person2)[2:-2],
               'commit2':unicode(commit2)[2:-2],
               'person3':unicode(person3)[2:-2],
			   'commit3': unicode(commit3)[2:-2],
	}
	
	#if your returning something new always make sure to include the new class ('text','value' etc)into the html or css

	   
        