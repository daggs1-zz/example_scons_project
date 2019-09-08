from SCons.Script import *
import os, glob
 
unpack_builder = Builder(action=[ "@echo unpacking `echo ${SOURCE.filebase} | sed 's/\.[^.]*$//;s/-/ \(version /g'`\)...", "@rm -rf ${TARGET}", "@tar xf ${SOURCE.abspath} -C ${TARGET.dir}", "mkdir ${TARGET}/.scons_build_stages" ])


def get_stages_folder_name():
	return '.scons_build_stages'

def prepare_env(env, pkg_name):
	src_tar_path = sorted(glob.glob(Dir(env['SRCS_FOLDER']).abspath + '/' + pkg_name + '-*'))[-1]
	tar_file_path = File(src_tar_path).abspath
	if not os.path.isfile(tar_file_path):
		raise SCons.Errors.UserError, "%s file was not found." %tar_file_path
	
	folder = os.popen("tar tvf " + tar_file_path + " 2>/dev/null | head -1 | awk '{print $NF}' | tr -d '\n'").read()
	
	if not len(folder):
		raise SCons.Errors.UserError, "%s is invalid." %tar_file_path
	env['unpacked_path'] = env.subst('$O') + '/' + folder
	env['src_tar_path'] = src_tar_path

def unpack(env, pkg_name):
	r = env.unpack(Dir(env['unpacked_path']), File(env['src_tar_path']))
	if not r:
		raise SCons.Errors.UserError, "failed to extract %s." %File(env['src_tar_path']).abspath

def patch(env, pkg_name):
	raise SCons.Errors.UserError, "unimplemented"

def prepare(env, pkg_name):
	raise SCons.Errors.UserError, "unimplemented"

def compile(env, pkg_name):
	raise SCons.Errors.UserError, "unimplemented"

def install(env, pkg_name):
	raise SCons.Errors.UserError, "unimplemented"

def init_utils_env(env):
    return env.Clone(BUILDERS = {'unpack' : unpack_builder})
