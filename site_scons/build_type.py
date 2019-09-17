# pkg build type

from enum import IntEnum

class type(IntEnum):
	CONFIGURE = 0
	KBUILD = 1
	UNSUPPORTED = 2
