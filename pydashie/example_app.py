from example_samplers import *

def run(app, xyzzy):
    samplers = [
        #BuiltJenkins(xyzzy, 3),
        #BuzzwordsSampler(xyzzy, 2), # 10
        #ConvergenceSampler(xyzzy, 1),
        ActiveIncidentsJiraSampler(xyzzy, 60),
        JenkinsSampler(xyzzy, 60),
		#ConfluenceReleaseNumberSampler(xyzzy,5),
		
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
