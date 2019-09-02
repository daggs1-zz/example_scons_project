from SCons.Script import *
import os
 
unpack = Builder(action="tar xaf ${SOURCE.abspath} -C ${TARGET.dir}")
util_env = Environment(BUILDERS = { "unpack": unpack, })
 
def unpack_src(dst_path, tar_file):
    if not os.path.isfile(tar_file):
        raise SCons.Errors.UserError, "%s file was not found." %tar_file
 
    r = util_env.unpack(dst_path, tar_file)
    if not r:
        raise SCons.Errors.UserError, "failed to extract %s." %tar_file
