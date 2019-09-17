# pkg build type

from enum import IntEnum

class type(IntEnum):
	CONFIGURE = 0
	KBUILD = 1
	MAKEFILE = 2
	UNSUPPORTED = 3
