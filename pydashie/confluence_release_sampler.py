from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime


"""
class ConfluenceReleaseNumberSampler(DashieSampler):

    def name(self):
      return 'releasenumber'
  
    def sample(self):
        wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Web+Home%3A+NHS+Spine+II+Wiki", auth=('emma.holmes', 'loopyloo'), verify=False)

        currentLiveReleasePattern = "\<pre\sid\='currentLiveRelease'\>(.*?)</pre>"
        matches = re.search (currentLiveReleasePattern, wikiHome.text)
        print matches
        print matches.group(0)
        releaseTable = matches.group(1)
        print releaseTable
   """    