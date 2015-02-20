from dashie_sampler import DashieSampler

import random
import requests
import collections

class TriageAssignedJiraSampler(DashieSampler):

    SEVERITY_KEY = ['fields','customfield_10009','value']
    SUMMARY_KEY = ['fields', 'summary']
    ISSUE_KEY = ['key']

    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'triageassigned'

    def _findByKey(self, val, keys):

        if len(keys) == 0:
            return val

        return self._findByKey(val[keys[0]], keys[1:])

    def _parseRequest(self, json):

        return {
            'label': self._findByKey(json, self.ISSUE_KEY),
            'value': self._findByKey(json, self.SUMMARY_KEY),
            'importanceLabel': self._findByKey(json, self.SEVERITY_KEY),
            'importanceValue': random.choice([1,2,3])
        }

    def sample(self):
        r = requests.get('http://localhost:8080/jira/triage_assigned.json', auth=('user', 'pass'))           
        return {'items': [self._parseRequest(issue) for issue in r.json()['issues']]}

class JenkinsSampler(DashieSampler):

    def __init__(self, *args, **kwargs):
        DashieSampler.__init__(self, *args, **kwargs)

    def name(self):
        return 'jenkins'

    def sample(self):
        # r = requests.get('http://localhost:8080/jira/triage_assigned.json', auth=('user', 'pass'))           
        # return {'items': [self._parseRequest(issue) for issue in r.json()['issues']]}
        return {'items': [{ 'label': 'test', 'value': 'tets val' }] }


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
