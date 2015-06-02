from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime



class ConfluenceCutFromDevelopAndRelease(DashieSampler):
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
	
    def name(self):
      return 'confluencecutdatesandrelease'
	#name is the link to the main.html
  
    def sample(self):
        wikiHome = requests.get("https://nhss-confluence.bjss.co.uk/display/SPINE/Web+Home%3A+NHS+Spine+II+Wiki", auth=('emma.holmes', 'loopyloo'), verify=False)
        #wikihome is the url where the information is
		
        currentLiveReleasePattern = "\<pre\sid\='currentLiveRelease'\>(.*?)</pre>"
        nextLiveRelease = "\<pre\sid\='nextLiveRelease'\>(.*?)</pre>"
        currentReleaseVersion = "\<pre\sid\='version0'\>(.*?)</pre>"
        currentReleaseDate = "\<pre\sid\='cutDate0'\>(.*?)</pre>"
		#Using the corresponding tags for the information you want
		
        matchescurrent = re.search (currentLiveReleasePattern, wikiHome.text)
        matchesnext = re.search (nextLiveRelease, wikiHome.text)
        matchesversion = re.search (currentReleaseVersion, wikiHome.text)
        matchesdate = re.search (currentReleaseDate, wikiHome.text)
		#re.search searches the wikihome and the tags above to find the data
		
        releaseCurrent = matchescurrent.group(1)
        releaseNext = matchesnext.group(1)
        releaseVersion = matchesversion.group(1)
        releaseDate = matchesdate.group(1)
		#.group(1) returns the first bit of info related to the tag (if you get and error about no groups in the terminal it might no matches were found (check tags))
		
        return {'text': releaseCurrent,
                'value': releaseNext,
                'label': "Cut From Develop",
                'writing': releaseVersion,
                'data': releaseDate, 
            }
		#if your returning something new always make sure to include the new class ('text','value' etc)into the html or css