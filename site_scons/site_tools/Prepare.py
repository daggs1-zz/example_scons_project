# prepare builder

from pathlib2 import Path
from os import path
from enum import IntEnum
from SCons.Script import *
import fnmatch, re

class build_type(IntEnum):
	KBUILD = 0
	UNSUPPORTED = 1

def prep_kbuild_pkg(pkg_name, work_dir, env, stages_folder):
	config = env.Command(work_dir + '/.config',
			     env.subst('$CONFIGS_FOLDER') + '/' + pkg_name + '.config',
			     Copy("$TARGET", "$SOURCE"))

	run_oldconfig = env.Make(Dir(stages_folder).abspath + '/oldconfig', config,
				 pkg_name = pkg_name, work_dir = work_dir,
				 single_job = True, implicit = True, make_targets = 'oldconfig')

	return [ config, run_oldconfig ]

build_types_handlers = [ (prep_kbuild_pkg, "(Config(|\..*)|Kconfig(|\..*))") ]

def get_all_regex():
	output = ""

	for type in build_type:
		if type == build_type.UNSUPPORTED:
			break
		output += build_types_handlers[int(type)][1] + '|'

	if len(output) > 1:
		output = output[:-1]

	return output

def parse_args(target, source, env):
	pkg_name = env.subst(str(env['pkg_name']))
	work_dir = env.subst(str(env['work_dir']))
	stages_folder = ""

	if 'stages_folder' in env.Dictionary().keys():
		stages_folder = env.subst(str(env['stages_folder']))

	return (pkg_name, work_dir, stages_folder)

def message(target, source, env):
	(pkg_name, work_dir, stages_folder) = parse_args(target, source, env)
	return "Preparing " + pkg_name + "..."

def builder(target, source, env):
	(pkg_name, work_dir, stages_folder) = parse_args(target, source, env)
	fmt = get_all_regex()
	files_list = sorted([f for f in os.listdir(Dir(work_dir).abspath) if re.match(r'^' + fmt + '$', f)])
	b_type = build_type.UNSUPPORTED
	ret_val = 1

	for file in files_list:
		for type in build_type:
			if type == build_type.UNSUPPORTED:
				break

			if re.match(r'^' + build_types_handlers[int(type)][1]  + '$', file):
				b_type = type
				break

	if b_type == build_type.UNSUPPORTED:
		print("unspported build type")
	else:
		deps = build_types_handlers[int(b_type)][0](pkg_name, work_dir, env, stages_folder)
		Path(target[0].abspath).touch()
		target = deps + target

		ret_val = 0

	return ret_val

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Prepare' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
