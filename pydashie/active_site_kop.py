import collections
import datetime
import random

from dashie_sampler import DashieSampler

class ActiveSite(DashieSampler):


    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'activesite'
    
    def sample(self):
        liveSite = 'x'
        return {'number':liveSite}