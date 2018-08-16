# codecapsule.py
#
'''
	This is the generic codecapsule class that is used for
	interactive code generation by operator overloading.
	Do not use this class directly; instead, subclass it to make

	- a given ISA (e.g., cc_8051.py, cc_thumb.py) common to all
		compilers for that ISA
		[this was extracted from the old codecapsule.py file]

	- a given ISA but specific to a compiler (e.g., cc_8051_iar.py,
		cc_8051_sdcc.py) that defines a calling convention
		[this is probably extracted from the old mapfile.py's API class?]

	- a given MCU (which is tied to an ISA) with its own specific 
	  usage of memory and resources
		[this is probably extracted from the old cc2540var.py and
		cc2540sfr.py?]
'''

from isa import ISA
import RPC


class CodeCapsule:
	'''this is the data structure for storing snippets of code that is
	   generated. this allows them to be emitted in order desired rather
	   than in order visited.

		 The following comments are obsolete -- they were specific to 8051
		 but now they are a mix, so ignore for now.

	   also need some kind of interface for the input and output of the
	   capsule. input = where the source is loaded (usually accumulator A,
	   could be register R0-R7, but there doesn't have to be any)
	   and output = where the result is placed (again, usually accumulator
	   A, could be register R0-R7, but doesn't have to be any)

		 Some modification is needed:
		 - indicate where the latest result is stored
		 - specify where the result should go:
		 - query type of result
		 For type and representation
		 - Byte: A (default), a register, a direct address, an
		   indirect address (thru @R0), an xdata address (thru
		   DPTR) (internal) stack relative (thru SP), and
			 constant value (R-value only)
		 - Bit: C (default), B.0, B.1, ... bit addressable
			 area, and constant value (R-value only)
		 - Word: tuple of locations?
		 - array: pointer, element type, number of elements
		 - struct: tuple of data types
	'''

	# important: all subclasses must define its own constructor to use
	# by redefining the following class variable.
	# an example would be for cc_8051.py's codecapsule subclass to
	# _isa_constructor = isa_8051.ISA8051

	_isa_constructor = ISA
	_instr_size = 1

	def __init__(self, mcu, dest=None, src=None):
		'''constructor: make an empty bag for code snippet.
		   can keep appending code and generate code.
			 possible uses
			 - designate where to place the destination (optional)
				 default is A for byte, C for bit, AB for 16-bit?
				 or follow IAR convention?  but can be anything?
				 => this dictates subsequent code generator to make
				 use of the designated var.  Code generators should
				 try to respect this.  A code capsule can change this
				 designation multiple times as it gets reused and
				 appended by different operators.
			 - retrieve where to find the latest result and type
			   (always possible) default is A for byte, C for bit.
				 12/18/2013
				 For 16-bit, we could use AB, but may be better to use
				 R3:R2 for this purpose, because this pair is used as
				 both the first 16-bit parameter as well as 16-bit return value.
				 It is easier because then if we make function calls, we don't
				 have to move it again.

				 A code generator can continue appending
				 code by taking the result from here and then output
				 to the designated place -- they can be different 
				 upon starting to append code, but after appending
				 code, it should be the same.

			- src is the destination in case the code capsule is just
			  a generic load.  For example, if you do P1._2, 
				P1 will result in a code capsule with a source = P1
				and dest = A, and then the codecapsule's getattr will
				return the source (=P1) to call the getattr on the _2 part.
				Then we throw away the code capsule (no need to load to A).
				However, if code is used in operator then src is set to None.
		  - there is one case that may need special handling, 
			  by looking for ANL/ORL/XRL direct, #data/A (atomic operation)
		'''
		self.__dict__['_mcu'] = mcu
		self.__dict__['_dest'] = dest
		self.__dict__['_src'] = src
		self.__dict__['_instructions'] = [ ]
		if dest is not None:
			self.__dict__['_resultType'] = dest.getVarType()
		else:
			self.__dict__['_resultType'] = None

	def send(self, code, retval_type):
		return self.__dict__['_mcu'].send(code, retval_type)

	def __coerce__(self, other):
		return (self, other)
	def __str__(self):
		mode = self.reprMode()
		if mode == 'exec':
			return repr(self)
		s =  self.getCode()
		if s is str:
			return s
		return str(s)

	def __getattr__(self, name):
		if (self.__dict__.has_key(name)):
			return self.__dict__[name]
		else:
			# pass the attribute access to the outlet?
			obj = self._src
			return obj.getattr(name)
	
	def __setattr__(self, name, value):
		if (self.__dict__.has_key(name)):
			self.__dict__[name] = value
		else:
			# pass attribute access to outlet
			obj = self._src
			print obj.setattr(name, value)

	def getDest(self):
		'''this is for a code generator to find out where to write the
		   value into.
		'''
		return self._dest

	def setDest(self, var):
		'''This is for a code-capsule maker to designate or change 
		   where someone should write the value into.
		'''
		self._dest = var
		self._resultType = var.getVarType()

	def getResultType(self):
		'''This lets an appender / user of this code capsule to query the
			type of the result.  Returns a string.'''
		return self._resultType

	def setResultType(self, resultType):
		'''This lets an appender / user of this code capsule to set the
			result type to what it code generates to.'''
		self._resultType = resultType

	def getRValue(self):
		'''This is for finding either which variable stores the latest
		   result, or if it is a constant.
		'''
		pass

	def emit(self, formatStr, *operands):
		# print "emit formatStr = ", formatStr, ", operands = ", operands
		self._instructions.append(self._isa_constructor(formatStr, *operands))

	def getMachineCode(self):
		# return reduce(lambda x,y: x+y, self._instructions)
		m = [ ]
		for i in self._instructions:
			m.append(i.machineCode())
		return m

	def __len__(self):
		'''get the length of the machine code, in bytes.
		   to make this work, define the class variable _instr_size = 1 or
			 some other size.
		'''
		return len(self.getMachineCode() * self._instr_size)

	def getCode(self):
		return self._instructions  ## or make a copy?

	def setCode(self, code):
		self._instructions = code

	def printCode(self):
		print '\n'.join(self._instructions)

	def appendCode(self, other):
		'''append the code list from another code capsule or instruction list
		'''
		L = self._instructions
		if isinstance(other, CodeCapsule):
			M = other.getCode()
		elif isinstance(other, list):
			M = other
		L[len(L):] = M

	def __repr__(self):
		'''
		This method is called by the interactive prompt at the top level to
		display a rendering of this object.  Our strategy is to generate a
		side-effect that sends the code to the node; if fast enough then we get a
		feedback.
		
		to implement this, we first clone one CodeCapsule object but with flattened
		instructions; and we also slap on some additional wrappers to grab the
		return value.
		'''
		if self._mcu.getAppendReturnBufCode():
			# clone = copy.deepcopy(self)
			clone=self
			clone.appendReturnValue()
		else:
			clone = self
		mode = self.reprMode()
		if (mode == 'text'):	
			return "%s(%s): %s" % \
				(clone.__class__.__name__, clone._dest, map(str, clone._instructions))
		# else assume binary
		# each instruction is a list of bytes. so, we should flatten them.
		# in python, [1,2]+[3,4] = [1,2,3,4],
		# so here we can just use the reduce() operator to "sum" them up
		# to effectively join these sublists.
		# return repr(clone.getMachineCode())
		machineCode = reduce(lambda x,y: x+y, clone.getMachineCode())
		if mode == 'exec':
			# this will need to be changed
			machineCode = machineCode + [0x22]
			retVal = self.send(machineCode, self.getResultType())
			return repr(RPC.demarshal(retVal, self.getResultType()))
			# return repr(retVal)
		if mode == 'binary':
			return "%d bytes: %s" % (len(machineCode), ['{0:08b}'.format(byte) for byte in machineCode])

		# else mode == 'exec'

	def setReprMode(self, mode):
		"""mode is 'text', 'binary', or 'exec'."""
		self._mcu.setReprMode(mode)

	def reprMode(self):
		return self._mcu.reprMode()

	def getReturnBufferAddress(self):
		'''This is a method for the address for the return value,
		   in order to return back to the user
		'''
		return self._mcu.getReturnBufferAddress()

	def setReturnBufferAddress(self, address):
		'''This is a method for setting the return buffer address'''
		self._mcu.setReturnBufferAddress(address)
