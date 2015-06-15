#importing the data from the correct file
from active_site_kop import*
from confluence_cut_from_develop_and_release import *
from confluence_merge_queue import *
from jenkins_built_count import*
from jenkins_building_count import*
from jenkins_failed_count import*
from jenkins_failed_other_priority_list import *
from jira_live_incidents import*
 
# Samplers and refresh rates are defined here 
def run(app, xyzzy):
    samplers = [
		ActiveSite(xyzzy, 2),
		ConfluenceCutFromDevelopAndRelease(xyzzy, 6),
		ConfluenceMergeQueue(xyzzy, 6),
        JenkinsBuiltCount(xyzzy, 3),
		JenkinsBuildingCount(xyzzy, 3),
		JenkinsFailedCount(xyzzy, 3),
		JenkinsFailedPriorityList(xyzzy, 3),		
		JiraLiveIncidents(xyzzy, 3),
		
			
		
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
