from jenkins_sampler import *
from jira_sampler import * 
#from confluence_release_sampler import *
from not_built_jenkins_sampler import *
from cut_from_develop_sampler import *
from merge_queue_sampler import *
from built_jenkins import*
from built_jenkins_list import*
from not_built_jenkins_count_sampler import*
from other_build_jenkins import*
from building_jenkins_count import*


 
# Samplers and refresh rates are defined here 
def run(app, xyzzy):
    samplers = [
        BuiltJenkins(xyzzy, 3),
		BuiltJenkinsSampler(xyzzy, 3),
        LiveIncidentsJiraSampler(xyzzy, 5),
        JenkinsSampler(xyzzy, 5),
		#ConfluenceReleaseNumberSampler(xyzzy, 5),
        CutFromDevelopSampler(xyzzy, 5),
        FailedJenkinsSampler(xyzzy, 5),
		MergeQueue(xyzzy, 5),
		FailJenkinsCount(xyzzy, 5),
		OtherJenkinsSampler(xyzzy,5),
		BuildingJenkinsCount(xyzzy,5)
		
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
