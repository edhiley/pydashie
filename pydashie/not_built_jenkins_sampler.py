import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests


""""

class BuiltJenkins(DashieSampler):

    STATUS_KEY = ['color']
    JOB_FILTER = 'blue'
    
    def __init__(self, *args, **kwargs):
         DashieSampler.__init__(self, *args, **kwargs)
        

    def name(self):
            return 'jenkinsbuilt'
        
    def _findByKey(self, val, keys):

            if len(keys) == 0:
                return val

            return self._findByKey(val[keys[0]], keys[1:])
        
    def _jobFilter(self, job):
    
            jobName = self._findByKey(job, self.STATUS_KEY)
            return self.JOB_FILTER in jobName
          
    def _parseRequest(self, json):
        
            status = self._findByKey(json, self.STATUS_KEY)
            current= self._findByKey(json, self.JOB_FILTER)
            
            return {
            'label': self.SEVERITY_LABEL_MAP[status],
            'value': self._findByKey(json, self.JOBS_KEY),
            'importanceLabel': self.SEVERITY_LABEL_MAP[status],
            'importanceValue': self.SEVERITY_MAP[status],
        }
               

    def sample(self):
        r = requests.get('http://nhss-aux.bjss.co.uk:8080/api/json?pretty=true', auth=('matthew.puzey', 'vertebrae'))
        jobs = r.json()['jobs']
               
        return sum(JOB_FILTER)[status]
"""