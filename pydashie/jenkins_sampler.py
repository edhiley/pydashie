import collections
import datetime
import random
import re 

from dashie_sampler import DashieSampler
import requests


class JenkinsSampler(DashieSampler):

    JOBS_KEY = ['name']
    STATUS_KEY = ['color']
    SEVERITY_MAP = {
        'red': '1',
        'notbuilt': '2',
        'blue_anime': '11',
        'blue': '11',
        'disabled': '5',
        'yellow': '6',
        'red_anime': '7',
        'aborted':'9',
        'yellow_anime': '6',
    }
    SEVERITY_LABEL_MAP = {
        'red': 'Failed',
        'notbuilt': 'Not Built',
        'blue_anime': 'Building',
        'blue': 'Built',
        'disabled': 'Disabled',
        'yellow': 'Unstable',
        'red_anime':'Failed-In Progress',
        'notbuilt_anime' : 'Not Built-In Progress',
        'aborted' : 'Aborted',
        'yellow_anime': 'Unstable-In Progress',
    }
    JOB_FILTER = 'spineii-main'
    
    

    def name(self):
        return 'jenkins'
            
            
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
        
        status = self._findByKey(json, self.STATUS_KEY)
        
        jobName = self._findByKey(json, self.JOBS_KEY)
        
                
        return {
            'label': self.SEVERITY_LABEL_MAP[status],
            'value': self._findByKey(json, self.JOBS_KEY),
            'importanceLabel': self.SEVERITY_LABEL_MAP[status],
            'importanceValue': self.SEVERITY_MAP[status],
        }

    def sample(self):
        r = requests.get('http://nhss-aux.bjss.co.uk:8080/api/json?pretty=true', auth=('matthew.puzey', 'vertebrae'))
        jobs = r.json()['jobs']
        return {'items': [self._parseRequest(job) for job in jobs if self._jobFilter(job)]}