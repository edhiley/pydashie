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

        # We need the version and the cut date for each entry in the table (rows shall be added as we go on we do not bother with crossed out first row) 
        currentReleaseVersion = "\<pre\sid\='version0'\>(.*?)</pre>"
        currentReleaseDate = "\<pre\sid\='cutDate0'\>(.*?)</pre>"
        # Are we able to search for multiple entries at once using the regular expression re.search?
        matches = re.search (currentReleaseVersion, wikiHome.text)
        match = re.search ()
        print matches
        print matches.group(0)
        releaseTable = matches.group(1)
        print releaseTable
        return {"text": releaseTable}
