#from jenkins_sampler import *
from jira_sampler import * 
from confluence_release_sampler import *
from not_built_jenkins_sampler import *
from cut_from_develop_sampler import *
from merge_queue_sampler import *
from built_jenkins import*
#from built_jenkins_list import*
from not_built_jenkins_count_sampler import*
#from other_build_jenkins import*
from building_jenkins_count import*
from active_site_kop import*
 
# Samplers and refresh rates are defined here 
def run(app, xyzzy):
    samplers = [
        BuiltJenkins(xyzzy, 30),
		#BuiltJenkinsSampler(xyzzy, 60),
        LiveIncidentsJiraSampler(xyzzy, 30),
        #JenkinsSampler(xyzzy, 60),
		ConfluenceReleaseNumberSampler(xyzzy, 60),
        CutFromDevelopSampler(xyzzy, 60),
        FailedJenkinsSampler(xyzzy, 30),
		MergeQueue(xyzzy, 60),
		FailJenkinsCount(xyzzy, 30),
		#OtherJenkinsSampler(xyzzy,60),
		BuildingJenkinsCount(xyzzy, 30),
        ActiveSite(xyzzy, 2),
		
    ]

    try:
        app.run(host='0.0.0.0',
                debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True
                )
    finally:
        print "Disconnecting clients"
        xyzzy.stopped = True
        
        print "Stopping %d timers" % len(samplers)
        for (i, sampler) in enumerate(samplers):
            sampler.stop()

    print "Done"
