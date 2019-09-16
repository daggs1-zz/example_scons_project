# configure builder

from pathlib2 import Path
import subprocess
from SCons.Script import *

def parse_args(target, source, env):
	pkg_name = env.subst(str(env['pkg_name']))
	work_dir = env.subst(str(env['work_dir']))
	dest_dir = env['ENV']['DESTDIR']

	return (pkg_name, work_dir, dest_dir)

def message(target, source, env):
	(pkg_name, work_dir, dest_dir) = parse_args(target, source, env)

	return "Configuring " + pkg_name + "..."

def builder(target, source, env):
	(pkg_name, work_dir, dest_dir, ) = parse_args(target, source, env)

	cmd = './configure --prefix=' + dest_dir

	configure = subprocess.Popen(cmd.split(" "),
				     cwd = Dir(work_dir).abspath,
				     stdout = subprocess.PIPE,
				     stderr = subprocess.STDOUT,
				     bufsize = 0)

	# see http://stackoverflow.com/questions/1183643/unbuffered-read-from-process-using-subprocess-in-python/1183654#1183654
	line = configure.stdout.readline()
	while line:
		print line.rstrip()
		line = configure.stdout.readline()

	if not configure.returncode:
		Path(target[0].abspath).touch()

	return configure.returncode

def generate(env, **kwargs):
	env.Append(BUILDERS = { 'Configure' : env.Builder(action = env.Action(builder, message)) })

def exists(env):
	return True
