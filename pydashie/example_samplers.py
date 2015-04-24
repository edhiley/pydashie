from dashie_sampler import DashieSampler

import random
import requests
import collections

#class ConfluenceMergeQueueSampler(DashieSampler):

   #ID_KEY = ['fields', 'body', 'view', 'value']
    #SUMMARY_KEY = ['fields', 'summary']
    #SEVERITY_MAP = {
      #  '1 Critical': '9',
       # '2 Major': '10',
       # '3 Important': '11',
       # '4 Minor': '12',
       # '5 Low': '13',
   # }
    #ISSUE_KEY = ['key']

    #def __init__(self, *args, **kwargs):
       # DashieSampler.__init__(self, *args, **kwargs)

    #def name(self):
     #   return 'mergequeue'

    #def _findByKey(self, val, keys):

      # if len(keys) == 0:
          #  return val
            
        #print val[keys[0]], keys[1:]

      #  return self._findByKey(val[keys[0]], keys[1:])
        
    #def _parseRequest(self, json):
      #  status = self._findByKey(json, self.ID_KEY)
        
        #return {
      #      'label': self._findByKey(json, self.ID_KEY),
           # 'value': self._findByKey(json, self.SEVERITY_KEY),
           # 'value': self._findByKey(json, self.SUMMARY_KEY),
           # 'importanceLabel': self.SEVERITY_MAP[status],
            #'importanceValue': self.SEVERITY_MAP[status],
       #   }

   # def sample(self):
        #r = requests.get('http://localhost:8080/jira/triage_assigned.json', auth=('user', 'pass'))
        #r = requests.get('http://localhost:8080/confluence/merge_queue.json', auth=('user', 'pass'))   
        #return {'items': [self._parseRequest(issue) for issue in r.json()['id']]}
       
class ActiveIncidentsJiraSampler(DashieSampler):

    SEVERITY_KEY = ['fields', 'customfield_10009', 'value']
    SUMMARY_KEY = ['fields', 'summary']
    SEVERITY_MAP = {
        '1 Critical': '9',
        '2 Major': '10',
        '3 Important': '11',
        '4 Minor': '12',
        '5 Low': '13',
    }
    ISSUE_KEY = ['key']

    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'activeincidents'

    def _findByKey(self, val, keys):

        if len(keys) == 0:
            return val
            
        #print val[keys[0]], keys[1:]

        return self._findByKey(val[keys[0]], keys[1:])
        
    def _parseRequest(self, json):
        status = self._findByKey(json, self.SEVERITY_KEY)
        
        return {
            'label': self._findByKey(json, self.ISSUE_KEY),
            'value': self._findByKey(json, self.SEVERITY_KEY),
            'value': self._findByKey(json, self.SUMMARY_KEY),
            'importanceLabel': self.SEVERITY_MAP[status],
            'importanceValue': self.SEVERITY_MAP[status],
          }

    def sample(self):
        #r = requests.get('http://localhost:8080/jira/triage_assigned.json', auth=('user', 'pass'))
        r = requests.get('http://localhost:8080/jira/jira_active_incidents.json', auth=('user', 'pass'))   
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
		'nobuilt_anime':'8',
        'aborted':'9'
    }
    SEVERITY_LABEL_MAP = {
        'red': 'Failed',
        'notbuilt': 'Not Built',
        'blue_anime': 'Building',
        'blue': 'Built',
        'disabled': 'Disabled',
		'yellow': 'Unstable',
		'red_anime':'Failed-In Progress',
		'nobuilt_anime' : 'Not Built-In Progress',
        'aborted' : 'Aborted'
    }
    JOB_FILTER = ['spineii-main-caredatadownloader','spineii-main-ci','spineii-main-ci-latest-os-patches',\
    'spineii-main-ci-latest-os-patches-ui','spineii-main-demographicspineapplication','spineii-main-everything'\
    ,'spineii-main-everything-sonar','spineii-main-operationsadminservice','spineii-main-overnight',\
    'spineii-main-overnight-repeatable-tests','spineii-main-prescriptionsadmin','spineii-main-selfservice'\
    ,'spineii-main-sonar-all-projects','spineii-main-spinealertservice','spineii-main-spinereportingservice'\
    ,'spineii-main-summarycarerecord']
    
    

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
        return jobName in self.JOB_FILTER

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



class SynergySampler(DashieSampler):
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)
        self._last = 0

    def name(self):
        return 'synergy'

    def sample(self):
        s = {'value': random.randint(0, 100),
             'current': random.randint(0, 100),
             'last': self._last}
        self._last = s['current']
        return s

class BuzzwordsSampler(DashieSampler):
    def name(self):
        return 'buzzwords'

    def sample(self):
        my_little_pony_names = ['Rainbow Dash',
                                'Blossomforth',
                                'Derpy',
                                'Fluttershy',
                                'Lofty',
                                'Scootaloo',
                                'Skydancer']
        items = [{'label': pony_name, 'value': random.randint(0, 20)} for pony_name in my_little_pony_names]
        random.shuffle(items)
        return {'items':items}

class ConvergenceSampler(DashieSampler):
    def name(self):
        return 'convergence'

    def __init__(self, *args, **kwargs):
        self.seedX = 0
        self.items = collections.deque()
        DashieSampler.__init__(self, *args, **kwargs)

    def sample(self):
        self.items.append({'x': self.seedX,
                           'y': random.randint(0,20)})
        self.seedX += 1
        if len(self.items) > 10:
            self.items.popleft()
        return {'points': list(self.items)}
