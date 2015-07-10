from dashie_sampler import DashieSampler
import requests
import collections
import datetime
import random
import re 

#this is not working yet it need to figure out where to get the info from 

class ActiveSite(DashieSampler):


    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'activesite'
    
    def sample(self):
        liveSite = 'x'
        return {'number':liveSite}