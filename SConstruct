import os, multiprocessing

# define std pathes
path = ['/usr/local/sbin', '/usr/local/bin',
	'/usr/sbin', '/usr/bin', '/sbin', '/bin']

SetOption('num_jobs', multiprocessing.cpu_count() + 1)

env = Environment(T="#/output/$flavor/target",
		  O="#/output/$flavor/build",
		  ENV={'PATH': path},
		  flavor="debug",
		  ROOT='#', SRCS_FOLDER='#/src')

if "src" in BUILD_TARGETS:
	env['src_targets'] = ARGUMENTS.get('targets', 0)
	SConscript('src/SConscript', variant_dir="$O",
		   duplicate=0, exports='env')
