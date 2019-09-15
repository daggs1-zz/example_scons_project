# prepare builder

from pathlib2 import Path
from os import path
from enum import IntEnum
from SCons.Script import *

class build_type(IntEnum):
	KBUILD = 0
	UNSUPPORTED = 1

def get_list_of_file_in_folder(work_dir):
	folder_content = os.listdir(work_dir)
	files_list = list()

	for entry in folder_content:
		abs_path = os.path.join(work_dir, entry)
		if not os.path.isdir(abs_path):
			files_list.append(abs_path)

	return files_list

def prep_kbuild_pkg(pkg_name, work_dir, env, stages_folder):
	config = env.Command(work_dir + '/.config',
			     env.subst('$CONFIGS_FOLDER') + '/' + pkg_name + '.config',
			     Copy("$TARGET", "$SOURCE"))

	run_oldconfig = env.Make(Dir(stages_folder).abspath + '/oldconfig', config,
				 pkg_name = pkg_name, work_dir = work_dir,
				 single_job = True, implicit = True, make_targets = 'oldconfig')

	return [ config, run_oldconfig ]

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
	files_list = get_list_of_file_in_folder(Dir(work_dir).abspath)
	b_type = build_type.UNSUPPORTED
	ret_val = 1
	cbs = [ prep_kbuild_pkg ]

	for file in files_list:
		fn = path.basename(file)
		if fn.startswith("Config.") or fn == "Config" or fn.startswith("Kconfig.") or fn == "Kconfig":
			b_type = build_type.KBUILD
			break

	if b_type == build_type.UNSUPPORTED:
		print("unspported build type")
	else:
		deps = cbs[int(b_type)](pkg_name, work_dir, env, stages_folder)
		Path(target[0].abspath).touch()
		target = deps + target

		ret_val = 0

	return ret_val

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Prepare' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
