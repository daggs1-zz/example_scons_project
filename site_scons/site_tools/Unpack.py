# unpack builder

import tarfile, re
from pathlib2 import Path
from SCons.Script import *

def parse_args(target, source, env):
	pkg_name = env.subst(str(env['pkg_name']))
	dest_dir = env.subst(str(env['dest_dir']))
	src_tar_path = source[0].abspath

	return (pkg_name, dest_dir, src_tar_path)

def message(target, source, env):
	(pkg_name, dest_dir, src_tar_path) = parse_args(target, source, env)
	fn = os.path.basename(src_tar_path)
	version = re.sub(r"\.tar\..*$|\.tgz$", "", fn[len(pkg_name) + 1:])
	return "unpacking " + pkg_name + " (" + version + ") into " + Dir(dest_dir).abspath

def builder(target, source, env):
	(pkg_name, dest_dir, src_tar_path) = parse_args(target, source, env)
	source_tar = tarfile.open(src_tar_path, 'r')
	source_tar.extractall(path = Dir(dest_dir).abspath)
	source_tar.close()
	Path(target[0].abspath).touch()

	return 0

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Unpack' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
