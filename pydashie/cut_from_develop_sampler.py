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
        currentLiveReleasePattern = "\<pre\sid\='currentLiveRelease'\>(.*?)</pre>"
        nextLiveRelease = "\<pre\sid\='nextLiveRelease'\>(.*?)</pre>"
        currentReleaseVersion = "\<pre\sid\='version0'\>(.*?)</pre>"
        currentReleaseDate = "\<pre\sid\='cutDate0'\>(.*?)</pre>"
        matches = re.search (currentLiveReleasePattern, wikiHome.text)
        match = re.search (nextLiveRelease, wikiHome.text)
        matchesa = re.search (currentReleaseVersion, wikiHome.text)
        matchb = re.search (currentReleaseDate, wikiHome.text)
        releaseCurrent = matches.group(1)
        releaseNext = match.group(1)
        releaseaCurrent = matchesa.group(1)
        releaseDate = matchb.group(1)
        return {'text': releaseCurrent,
				'value': releaseNext,
				'label': "Cut From Develop",
				'writing': releaseaCurrent,
                'data': releaseDate,
				
                
            }

            
