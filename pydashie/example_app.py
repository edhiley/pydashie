from jenkins_sampler import *
from jira_sampler import * 
from confluence_release_sampler import *
from not_built_jenkins_sampler import *
from cut_from_develop_sampler import *

 
# Samplers and refresh rates are defined here 
def run(app, xyzzy):
    samplers = [
        #BuiltJenkins(xyzzy, 3),
        LiveIncidentsJiraSampler(xyzzy, 60),
        JenkinsSampler(xyzzy, 60),
		ConfluenceReleaseNumberSampler(xyzzy, 5),
        #CutFromDevelopSampler(xyzzy, 2),
        FailedJenkinsSampler(xyzzy, 60)
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
