import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests


class BuiltJenkinsSampler(DashieSampler):

    JOBS_KEY = ['name']
    STATUS_KEY = ['color']
    #AUTHOR_KEY_MAP={ 'Joseph Partridge': 'Joeseph Partridge',}
    #AUTHOR_KEY=['lastBuild', 'changeSet', 'items', 'author', 'fullName']
    SEVERITY_MAP = {
        
        'blue': '11',
        
    }
    SEVERITY_LABEL_MAP = {
        
        'blue': 'Built',
        
    }
    JOB_FILTER = ''
      

    def name(self):
        return 'builtjenkinslist'
            
            
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
 
    def _findByKey(self, val, keys):

        if len(keys) == 0:
            return val

        return self._findByKey(val[keys[0]], keys[1:])
        
    def _jobFilter(self, job):
    
        jobName = self._findByKey(job, self.JOBS_KEY)
        return self.JOB_FILTER in jobName

    def _parseRequest(self, json):
    #author = self._findByKey(json, self.AUTHOR_KEY)
        STATUS_FILTER = 'blue'
        status = self._findByKey(json, self.STATUS_KEY)
        if status == STATUS_FILTER:                
            return {
                'label': self.SEVERITY_LABEL_MAP[status],
                'value': self._findByKey(json, self.JOBS_KEY),
                #'text': self.AUTHOR_KEY_MAP[author],
                'importanceLabel': self.SEVERITY_LABEL_MAP[status],
                'importanceValue': self.SEVERITY_MAP[status],
            }
        else:
            return ""
    
    
    def sample(self):
        r = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true', auth=('joel.bywater', 'vertebrae'))
        jobs = r.json()['jobs']
        return {'items': [self._parseRequest(job) for job in jobs if self._jobFilter(job)]}