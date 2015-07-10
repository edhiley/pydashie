from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime



class ConfluenceReleaseNumberSampler(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
      return 'releasenumber'
  
  
    def sample(self):
        wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Web+Home%3A+NHS+Spine+II+Wiki", auth=('emma.holmes', 'Welcome123'), verify=False)

        currentLiveReleasePattern = "\<pre\sid\='currentLiveRelease'\>(.*?)</pre>"
        nextLiveRelease = "\<pre\sid\='nextLiveRelease'\>(.*?)</pre>"
        matches = re.search (currentLiveReleasePattern, wikiHome.text)
        match = re.search (nextLiveRelease, wikiHome.text)
        #print matches
        #print matches.group(0)
        releaseCurrent = matches.group(1)
        releaseNext = match.group(1)
        #print releaseCurrent
        print releaseNext
        print releaseCurrent
        return {'text': releaseCurrent,
                'value': releaseNext,

            }
        
