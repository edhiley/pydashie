from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime

class MergeQueue(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self): 
      return 'mergequeue'
  
  
    def sample(self):
       wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Merge+Queue", auth=('emma.holmes', 'loopyloo'), verify=False)
       matches= re.findall ('<td colspan="1" class="confluenceTd">(.*?)</td>',wikiHome.text)
       match=matches[0:1]
       match2=matches[4:5]
       match3=matches[8:9]
       return {'text': unicode(match)[3:-2],
				'value':unicode(match2)[3:-2],
				'writing': unicode(match3)[3:-2],
				 
		}

	   
        