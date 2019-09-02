import os
 
# define std pathes
path = ['/usr/local/sbin', '/usr/local/bin', '/usr/sbin', '/usr/bin', '/sbin', '/bin']
env = Environment(T = "#/output/$flavor/binaries", O = "#/output/$flavor/objects", ENV = {'PATH' : path}, flavor = "debug", ROOT = os.environ['PWD'])
 
SConscript('src/SConscript', variant_dir=Dir(env.subst('$O')).path, duplicate=0, exports='env')
