import collections
import datetime
import random
import re
from dashie_sampler import DashieSampler
import requests


class JenkinsFailedPriorityList(DashieSampler):

    JOBS_KEY = ['name']
    STATUS_KEY = ['color']
	#the above are keys in the api to bring back the correct data
	
    SEVERITY_MAP = {
        'red': '1',
        'notbuilt': '2',
        'disabled': '5',
        'yellow': '6',
        'red_anime': '7',
        'aborted':'9',
        'yellow_anime': '6',
    }
	
	
    #red= Image.open("/assets/images/Jenkins/red_ball.png")
    SEVERITY_LABEL_MAP = {
        'red':"Failed",
        'notbuilt': 'Not Built',
        'disabled': 'Disabled',
        'yellow': 'Unstable',
        'red_anime':'Failed-In Progress',
        'notbuilt_anime' : 'Not Built-In Progress',
        'aborted' : 'Aborted',
        'yellow_anime': 'Unstable-In Progress',
    }
	#the above make the information returned more readable( severity_map changes makes the background for each a different colour: look in prioritylist.scss)(severity_label_map changs the writing so the turned results make sense)
	
    JOB_FILTER = ''
	#this brings back all jobs in the filter used in api
      

    def name(self):
        return 'failedjenkinsprioritylist'
    #name is the link to the main.html           
            
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

        STATUS_FILTER = 'red'
        STAT_FILTER = 'red_anime'
        STATUS_FILTER1 = 'notbuilt'
        STATUS_FILTER2 = 'disabled'
        STATUS_FILTER3 = 'yellow'
        STATUS_FILTER4 ='aborted'
        STATUS_FILTER5 ='yellow_anime'
		#the above filter the results that need to be returned
		
        status = self._findByKey(json, self.STATUS_KEY)
		#status is equal to the status_key so using the filters in the if statement only returns the information needed
        if status == STATUS_FILTER or status == STAT_FILTER or status == STATUS_FILTER1 or status == STATUS_FILTER2 or status == STATUS_FILTER3 or status == STATUS_FILTER4 or status == STATUS_FILTER5:               
            return {
                'lab1': self.SEVERITY_LABEL_MAP[status],
                'val1': self._findByKey(json, self.JOBS_KEY),
                'statusLabel': self.SEVERITY_LABEL_MAP[status],
                'statusValue': self.SEVERITY_MAP[status],
				        }
        else:
            return ""
		#if your returning something new always make sure to include the new class ('lab1','val1' etc)into the html or css
    
    
    def sample(self):
	#this is the api that the information is returned from
        r = requests.get('http://nhss-aux.bjss.co.uk:8080/view/Main%20Builds/api/json?pretty=true', auth=('emma.holmes11', 'vertebrae'))
        jobs = r.json()['jobs']
        return {'items': [self._parseRequest(job) for job in jobs if self._jobFilter(job)]}