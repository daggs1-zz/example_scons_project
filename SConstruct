import os
import utils

# define std pathes
path = ['/usr/local/sbin', '/usr/local/bin',
	'/usr/sbin', '/usr/bin', '/sbin', '/bin']

env = Environment(T="#/output/$flavor/binaries",
		  O="#/output/$flavor/objects",
		  ENV={'PATH': path},
		  flavor="debug",
		  ROOT='#',
		  SRCS_FOLDER='#/src')

SConscript('src/SConscript', variant_dir="$O",
	   duplicate=0, exports='env')
