from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime



class CutFromDevelopSampler(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
      return 'cutdates'
  
  
    def sample(self):
        wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Web+Home%3A+NHS+Spine+II+Wiki", auth=('emma.holmes', 'loopyloo'), verify=False)
        currentReleaseVersion = "\<pre\sid\='version0'\>(.*?)</pre>"
        currentReleaseDate = "\<pre\sid\='cutDate0'\>(.*?)</pre>"
        matchesa = re.search (currentReleaseVersion, wikiHome.text)
        matchb = re.search (currentReleaseDate, wikiHome.text)
        releaseaCurrent = matchesa.group(1)
        releaseDate = matchb.group(1)
        return {'writing': releaseaCurrent,
                'data': releaseDate,
				
                
            }

            
