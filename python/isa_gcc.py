#
# isa_gcc.py
#
# this is not really an ISA, but accepts C and calls avr-gcc to compile it
# (extend it later to use different C compilers as well, SDCC, msp-gcc, etc)
#

from isa import ISA
class ISAGCC(ISA):
	'''
		this is the data structure for generating code (assembly or machine) using GCC.
	'''
	_isa_name = "GCC"

	def __init__(self, formatStr, *argList):
		'''the constructor takes the format string, does a match, and
		arguments for assembly.
		Save both the assembled code (list of numbers = bytes) and
		the assembly string.'''
		self._str = eval("'" + formatStr + "' % " + str(argList))
		self._asm = None

	def __len__(self):
		return len(self.machineCode())

	def __str__(self):
		return self._str

	def __repr__(self):
		return self._str

	def machineCode(self):
		if self._asm == None:
			# TODO: write code to tmp file, call gcc, call objcopy, read binary, delete tmp files
			pass
		return self._asm
