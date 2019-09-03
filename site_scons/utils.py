from SCons.Script import *
import os
 
unpack = Builder(action=[ "rm -rf ${TARGET.dir}", "tar xf ${SOURCE.abspath} -C ${TARGET.dir.dir}", "touch ${TARGET.abspath}" ])#, target_factory=Dir)
# util_env = Environment(BUILDERS = { "unpack": unpack, })

def unpack_src(env, dst_path, tar_file):
	tar_file_path = File(tar_file).abspath
	if not os.path.isfile(tar_file_path):
		raise SCons.Errors.UserError, "%s file was not found." %tar_file_path

	folder = os.popen("tar tvf " + tar_file_path + " 2>/dev/null | head -1 | awk '{print $NF}' | tr -d '\n'").read()

	if not len(folder):
		raise SCons.Errors.UserError, "%s is invalid." %tar_file_path

	r = env.unpack(dst_path + '/' + folder + '.unpacked', tar_file)
	if not r:
		raise SCons.Errors.UserError, "failed to extract %s." %tar_file_path
