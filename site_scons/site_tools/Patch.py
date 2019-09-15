# patch builder

import subprocess, os
from pathlib2 import Path
from SCons.Script import *

def parse_args(target, source, env):
	pkg_name = env.subst(str(env['pkg_name']))
	dest_dir = Dir(env.subst(str(env['dest_dir']))).abspath
	patches_list = env.subst(str(env['patches_list'])).strip('[]\'')
	if len(patches_list):
		patches_list = patches_list.split(',')

	return (pkg_name, dest_dir, patches_list)

def message(target, source, env):
	(pkg_name, dest_dir, patches_path) = parse_args(target, source, env)
	if len(patches_path):
		return "Patching " + pkg_name + "..."
	else:
		return ""

def builder(target, source, env):
	(pkg_name, dest_dir, patches_list) = parse_args(target, source, env)
	ret_val = 0

	if patches_list:
		for patch in patches_list:
			print("Applying " + os.path.basename(patch) + "...")
			cmd = "patch -p0 -i " + patch + " -d " + Dir(dest_dir).abspath
			patch = subprocess.Popen(cmd.split(" "))
			output = patch.communicate()[0]

			if patch.returncode != 0:
				ret_val = patch.returncode
				break

	Path(target[0].abspath).touch()

	return ret_val

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Patch' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
