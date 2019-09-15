# make builder

from pathlib2 import Path
import subprocess
from SCons.Script import *

def parse_args(target, source, env):
	pkg_name = env.subst(str(env['pkg_name']))
	work_dir = env.subst(str(env['work_dir']))
	dest_dir = ""
	jobs = GetOption('num_jobs')
	implicit = False
	install_flow = False
	make_targets = ""

	if 'single_job' in env.Dictionary().keys() and env['single_job'] == True:
		jobs = 1

	if 'implicit' in env.Dictionary().keys():
		 implicit = env['implicit']

	if 'install' in env.Dictionary().keys():
		 install_flow = env['install']
		 dest_dir = env.subst(str(env['dest_dir']))
		 implicit = False

	if 'make_targets' in env.Dictionary().keys():
		make_targets = env.subst(str(env['make_targets']))

	return (pkg_name, work_dir, dest_dir, jobs, implicit, install_flow, make_targets)

def message(target, source, env):
	(pkg_name, work_dir, dest_dir, jobs, implicit, install_flow, make_targets) = parse_args(target, source, env)
	msg = ""

	if not implicit:
		if install_flow:
			msg = "Install"
		else:
			msg = "Build"

		msg += "ing " + pkg_name

		if len(make_targets) > 1:
			msg += " (targets: " + make_targets + ")"
		elif len(make_targets) == 1:
			msg += " (target: " + make_targets + ")"

		msg + "..."

	return msg

def builder(target, source, env):
	(pkg_name, work_dir, dest_dir, jobs, implicit, install_flow, make_targets) = parse_args(target, source, env)

	cmd = 'make -j ' + str(jobs)

	if install_flow:
		cmd += ' DESTDIR=\"' + dest_dir + '\" install'

	if len(make_targets) > 0:
		cmd += ' ' + make_targets

	make = subprocess.Popen(cmd.split(" "),
				cwd = Dir(work_dir).abspath)

	output = make.communicate()[0]

	if not make.returncode:
		Path(target[0].abspath).touch()

	return make.returncode

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Make' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
