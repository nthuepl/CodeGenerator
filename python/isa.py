#
# isa.py
#
# this is the base class for ISA.
# it just provides the methods used by all ISAs
#

class ISA:
	'''
		this is the data structure for generating code (assembly or machine)
		for 8051.  It is a "factory".  we define these formatting strings
		and formatting functions as either constant list or lambda to a
		list of expressions.  One can do code-gen and pattern match - but
		they should match exactly...  This also means we can't really do
		labels, but probably that could be solved later?
	'''
	_instr = { }
	_isa_name = ""
	def __init__(self, formatStr, *argList):
		'''the constructor takes the format string, does a match, and
		arguments for assembly.
		Save both the assembled code (list of numbers = bytes) and
		the assembly string.'''
		if not self._instr.has_key(formatStr):
			# print 'formatStr is = ', formatStr
			raise ValueError("%s is not a valid %s assembly format" % \
					(formatStr, self._isa_name))
		f = self._instr[formatStr]
		if isinstance(f, list):
			# not a lambda - so argList should be empty
			if (len(argList)):
				raise ValueError("%s takes no operand" % formatStr)
			# make a copy, save in assembly
			self._asm = f[:]
			self._str = formatStr
		else: # it's a lambda, let's evaluate it
			self._asm = apply(f, argList)
			self._str = eval("'" + formatStr + "' % " + str(argList))

	def __len__(self):
		return len(self._asm)

	def __str__(self):
		return self._str

	def __repr__(self):
		return self._str

	def machineCode(self):
		return self._asm

