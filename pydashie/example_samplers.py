"""
from dashie_sampler import DashieSampler

import random
import requests
import collections
import re 
import datetime

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
    
 	
     
class ActiveIncidentsJiraSampler(DashieSampler):

    SEVERITY_KEY = ['fields', 'customfield_10009', 'value']
    SUMMARY_KEY = ['fields', 'summary']
    TIME_KEY= ['fields', 'created']
    STATUS_KEY=['fields','status', 'name']
    SEVERITY_MAP = {
        '1 Critical': '1',
        '2 Major': '1',
        '3 Important': '10',
        '4 Minor': '11',
        '5 Low': '11',
        '': '12',
    }
    SEVERITY_LABEL_MAP = {
        '1 Critical': 'Sev 1',
        '2 Major': 'Sev 2',
        '3 Important': 'Sev 3',
        '4 Minor': 'Sev 4',
        '5 Low': 'Sev 5',
        '': 'Sev --',
		
	}
    ISSUE_KEY = ['key']
	

    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'activeincidents'

    def _findByKey(self, val, keys, default = None):

        if len(keys) == 0:
            return val 
            
        #print val[keys[0]], keys[1:]
        #print 'default = '.format(default)
        if not val or keys[0] not in val:
            return default
        else:
            return self._findByKey(val[keys[0]], keys[1:], default)
	       
    def _parseRequest(self, json):
        status = self._findByKey(json, self.SEVERITY_KEY, default='')
        severity = self._findByKey(json, self.ISSUE_KEY, default='')

        time = self._findByKey(json, self.TIME_KEY)
        return {
            'text': severity,
            'value': self._findByKey(json, self.SUMMARY_KEY),
			'label': self.SEVERITY_LABEL_MAP[status],
			'time': "%s.%s.%s" % (time[8:10],time[5:7], time[2:4]),
			'status': self._findByKey(json, self.STATUS_KEY),
            'importanceLabel': self.SEVERITY_MAP[status],
            'importanceValue': self.SEVERITY_MAP[status],
          }

    def sample(self):
        r = requests.get('https://nhss-jira.bjss.co.uk/rest/api/2/search?jql=(issuetype+%3D+Incident+AND+cf%5B10805%5D+%3D+live+OR+issuetype+%3D+%22Cherwell+Service+Request%22)+AND+status+not+in+(closed)+ORDER+BY+cf%5B10009%5D+ASC,+created+ASC ', auth=('matt.puzey', 'esabhm7j'), verify=False)  
       #print "Hello " + r.json() 
        print 'refresh'
        return {'items': [self._parseRequest(issue) for issue in r.json()['issues']]}
        

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