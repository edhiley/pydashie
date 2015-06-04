import collections
import datetime
import random
import re 
from datetime import datetime
from dashie_sampler import DashieSampler
import requests


class JiraLiveIncidents(DashieSampler):

    SEVERITY_KEY = ['fields', 'customfield_10009', 'value']
    SUMMARY_KEY = ['fields', 'summary']
    TIME_KEY= ['fields', 'created']
    STATUS_KEY=['fields','status', 'name']	
    ISSUE_KEY = ['key']
	#the above are keys in the api to bring back the correct data
	
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
	#the above make the information returned more readable( severity_map changes makes the background for each a different colour: look in prioritylist.scss)(severity_label_map changs the writing so the turned results make sense)
    
    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'jiraliveincidents'
	#name is the link to the main.html    

    def _findByKey(self, val, keys, default = None):

        if len(keys) == 0:
            return val 
            
        if not val or keys[0] not in val:
            return default
        else:
            return self._findByKey(val[keys[0]], keys[1:], default)
           
    def _parseRequest(self, json):
        
        status = self._findByKey(json, self.SEVERITY_KEY, default='')
        severity = self._findByKey(json, self.ISSUE_KEY, default='')
        time = self._findByKey(json, self.TIME_KEY)
		#creates easy ways to identify the keys
		
        date='%s-%-s-%s' % (time[8:10],time[5:7], time[2:4]),
		#because the result of bring back the date includes time and UTC etc have to be specific about which parts to bring back
        datestring= str(date)
		#converts it into a useable string
        datestring= datestring[3:-3]
		#makes sure only the right bits within the string are used
        date_object=datetime.strptime(datestring,'%d-%m-%y')
		#makes the string into the date format
        today=datetime.today().date()
		#todays date
        jiradate=datetime.date(date_object)
		#the date on the jira
        day= "day"
        daysplural="days"		
		#text to go on the end
        diff=((today-jiradate).days)
		#works out the amount of days the incident has been on Jira
        if diff ==1:
			result= str(diff) +day 
        else:
			result= str(diff) +daysplural 
		#end result plus the text dependant on days or day
		
		
		
        return {
            'status': self._findByKey(json, self.STATUS_KEY),
			'label': self.SEVERITY_LABEL_MAP[status],
			'text': severity,
			'time': result,
            'value': self._findByKey(json, self.SUMMARY_KEY),
            'importanceLabel': self.SEVERITY_MAP[status],
            'importanceValue': self.SEVERITY_MAP[status],
          }
	#if your returning something new always make sure to include the new class ('text','value' etc)into the html or css

    def sample(self):
	#this is the api that the information is returned from
        r = requests.get('https://nhss-jira.bjss.co.uk/rest/api/2/search?jql=(issuetype+%3D+Incident+AND+cf%5B10805%5D+%3D+live+OR+issuetype+%3D+%22Cherwell+Service+Request%22)+AND+status+not+in+(closed)+ORDER+BY+cf%5B10009%5D+ASC,+created+ASC ', auth=('matt.puzey', 'esabhm7j'), verify=False)  
        print 'refresh'
        return {'items': [self._parseRequest(issue) for issue in r.json()['issues']]}