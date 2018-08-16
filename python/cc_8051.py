#
# cc_8051.py
#

from codecapsule import CodeCapsule
import isa_8051
import RPC

#The following three functions still need to be changed to be 
# generic to 8051, rather than specific to cc2540

typeDef = {
			# size should always be in bits. to allow 12-bit or 14-bit
			# ADC values?  or should this be handled as bit field?
			'bool':           { 'size': 1,  'signed': False, 'align': False, },
			'char':           { 'size': 8,  'signed': True,  'align': False, },
			'unsigned char':  { 'size': 8,  'signed': False, 'align': False, },
			'char*':          { 'size': 16, 'signed': False, 'align': False, },
			'uint8':          { 'size': 8,  'signed': False, 'align': False, },
			'uint8*':         { 'size': 16, 'signed': False, 'align': False, },
			'int8':           { 'size': 8,  'signed': True,  'align': False, },
			'int8*':          { 'size': 16, 'signed': False, 'align': False, },
			'short':          { 'size': 16, 'signed': True,  'align': False },
			'unsigned short': { 'size': 16, 'signed': False, 'align': False },
			'uint16':         { 'size': 16, 'signed': False, 'align': False },
			'uint16*':        { 'size': 16, 'signed': False, 'align': False },
			'uint24':         { 'size': 24, 'signed': False, 'align': False },
			'long':           { 'size': 32, 'signed': True,  'align': False },
			'unsigned long':  { 'size': 32, 'signed': False, 'align': False },
			'uint32':         { 'size': 32, 'signed': False, 'align': False },
			## do we support floating point?
			}

def sizeInBits(typeName):
	#if not VAR._typeDef.has_key(typeName):
	#	raise TypeError('unknown type %s' % typeName)
	# look up number of bits
	if typeName[-1] == '*':
		return 16
	else:
		return typeDef[typeName]['size']

def isSigned(typeName):
	return typeDef[typeName]['signed']


def checkRange(value, bits, signed): # > 65535 or other < -32768):
	if signed:
		# value should be between -2^(n-1) and 2^(n-1) - 1
		lower = -(1 << (bits - 1))
		upper = (1 << (bits - 1)) - 1
	else:
		# value should be between 0 and 2^(n) - 1
		lower = 0
		upper = (1 << bits) - 1
	if (value < lower) or (value > upper):
		raise ValueError('%d-bit constant value %s out of range: should be %d..%d' \
					% (bits, value, lower, upper))

class CC_8051(CodeCapsule):
	'''
		This is the code capsule class for 8051.
		It inherits the generic structure of CodeCapsule class and provides
		the common code for interactive code generation for 8051 ISA.
		It inherits the constructor from the base class.
		Important to define the constructor to use.
	'''

	_isa_constructor = isa_8051.ISA8051

	def repr__(self):
		'''just a placeholder for now'''
		if self._mcu.getAppendReturnBufCode():
			clone = self
			clone.appendReturnValue()
		else:
			clone = self
		mode = self.reprMode()
		if (mode == 'text'):
			return "%s(%s): %s" % \
					(clone.__class__.__name__, clone._dest, map(str,
						clone._instructions))
		machineCode = clone.getMachineCode()
		if mode == 'exec':
			machineCode = reduce(lambda x, y: x+y, machineCode) + [0x22]
			retVal = self.send(machineCode, self.getResultType())
			return repr(RPC.demarshal(retVal, self.getResultType()))
		if mode == 'binary':
			return repr(reduce(lambda x, y: x+y, machineCode))


	def appendReturnValue(self):
		'''This method was moved from mapfile's grabReturnValue.
		   This one should be upgraded so it can support using
			 either iram or xdata for appending return value.
			 This one is currently using xdata because this is how
			 Neo has allocated it.  idata may be faster and shorter
			 code size.
		'''
		t = self.getResultType()
		self.emit('MOV DPTR, #0x%x', self.getReturnBufferAddress())
		if (t == 'void') or (t is None):
			# just set length = 0
			self.emit('CLR A')
			self.emit('MOVX @DPTR, A')
		elif (sizeInBits(t) == 1):
			# put C into A
			# self.emit('MOV A, #0x%x', 1)
			# self.emit('MOVX @DPTR, A')
			# self.emit('INC DPTR')
			self.emit('CLR A')
			self.emit('RLC A') # rotate the C bit left back into A.0
			# set length = 1
			self.emit('MOVX @DPTR, A')
		elif (sizeInBits(t) == 8):
			# self.emit('PUSH ACC') # save value of A
			# set length = 1
			# self.emit('MOV A, #0x%x', 1)
			# self.emit('MOVX @DPTR, A')
			# self.emit('INC DPTR')
			# self.emit('POP ACC')
			self.emit('MOVX @DPTR, A')
			# Modified 12/20/2013: use A for return value
			# (function calls return in R1, already copied to A)
		elif (sizeInBits(t) == 16):
			# set length = 2
			# self.emit('MOV A, #0x%x', 2)
			# self.emit('MOVX @DPTR, A')
			# self.emit('INC DPTR')
			self.emit('MOV A, R%d', 2)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 3)
			self.emit('MOVX @DPTR, A')
		elif (sizeInBits(t) == 24):
			# set length = 3
			# self.emit('MOV A, #0x%x', 3)
			# self.emit('MOVX @DPTR, A')
			# self.emit('INC DPTR')
			self.emit('MOV A, R%d', 1)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 2)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 3)
			self.emit('MOVX @DPTR, A')

		elif (sizeInBits(t) == 32):
			# set length = 4
			# self.emit('MOV A, #0x%x', 4)
			# self.emit('MOVX @DPTR, A')
			# self.emit('INC DPTR')
			# assuming use iram for buffer; move data from R2:R5 to buf[1:4]
			self.emit('MOV A, R%d', 2)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 3)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 4)
			self.emit('MOVX @DPTR, A')
			self.emit('INC DPTR')
			self.emit('MOV A, R%d', 5)
			self.emit('MOVX @DPTR, A')
		else:
			raise TypeError('return type %s not supported' % t)

	def allocTemp(self, temp=None):
		return self._mcu.allocTemp(temp)

	def freeTemp(self, obj):
		self._mcu.freeTemp(obj)


	def saveAinTemp(self, temp):
		'''saves accumulator A into temp. This is hardwired...
		 should generate code by assignment to handle different types
		'''
		self.emit('MOV R%d, A', temp.varAddress())

	def allocTempBit(self, temp=None):
		return self._mcu.allocTempBit(temp)

	def freeTempBit(self, obj):
		self._mcu.freeTempBit(obj)

	def saveCinTempBit(self, temp):
		self.emit('MOV 0x%x, C', temp.varAddress())

	def __add__(self, other):
		'''This overloads the + operator.  It assumes self and others have
		   been code-generated (or other can be an int).
			 This handles only 8-bit int for now. 
			 16-bit could be handled as function call to be easier.
			 If 8-bit is added with 16-bit then should promote 8-bit first.
		'''
		if isinstance(other, int) or isinstance(other, str):
			# maybe code capsule needs to add type?
			# to model what kind it is.
			# if it is in A, then just add A!!
			# check if int is 0. if so, skip it.
			if isinstance(other, str):
				if len(other) == 0:
					other = 0
				elif len(other) == 1:
					other = ord(other)
				else:
					raise ValueError('cannot (yet) add string')
			if (other != 0):
				# check range. Question: how to handle sign or unsigned? may need to
				# know on the host side when type-demarshaling?
				# should check self's type.
				t = self.getResultType();
				if sizeInBits(t) == 16: # was: == 'uint16' or t[-1] == '*':
					# need to pass the other to 16-bit, stick it into R5:R4 then call.
					# check range
					checkRange(other, 16, isSigned(t)) # > 65535 or other < -32768):
					# we can handle 16-bit add: just do LSB first, then ADDC
					self.emit('MOV A, R2')
					self.emit('ADD A, #0x%x', other & 0xff)
					self.emit('MOV R2, A')
					self.emit('MOV A, R3')
					self.emit('ADDC A, #0x%x', (other >> 8) & 0xff)
					self.emit('MOV R3, A')
				elif sizeInBits(t) == 8: # assume 8-bit, already in A. just do an add.
					checkRange(other, 8, isSigned(t))
					self.emit('ADD A, #0x%x', other)
				else:
					raise TypeError('unsupported type %s in + operator' % t)
				# set the result (R-Value and L-Value) to A?
				# write to the dest if it is not A?
			# else (other==0) skip.
		elif isinstance(other, CodeCapsule):
			# first, check if both 8-bit
			t1 = self.getResultType()
			t2 = other.getResultType()
			if sizeInBits(t1) == 8 and sizeInBits(t2) == 8:
				# do the first, save the result into a temporary, do the second,
				# and then add.
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('ADD A, R%d', temp.varAddress())
				self.freeTemp(temp)
			else:
				# promote 8 bit to 16 bit
				if sizeInBits(t1) == 16 and sizeInBits(t2) == 16:
					# push R2 and R3 on stack
					self.emit('PUSH 0x%x', 3)
					self.emit('PUSH 0x%x', 2)
					self.appendCode(other)
					self.emit('POP ACC')
					self.emit('ADD A, R%d', 2)
					self.emit('XCH A, R%d', 2)
					self.emit('POP ACC')
					self.emit('ADDC A, R%d', 3)
					self.emit('XCH A, R%d', 3)
				else:
					# will handle type promotion later
					raise TypeError('mixed %s + %s not yet supported' % (t1, t2))
		else:
			raise TypeError('unsupported type for +: %s' % type(other))
		return self

	def __radd__(self, other):
		'''add is commutative, so handle with regular add
		   e.g., 1 + mcu.R2 handled as mcu.R2 + 1
		'''
		return self.__add__(other)

	def __sub__(self, other):
		'''
		this works for x - y.  need to be careful with evaluation order
		in case of associativity
		x - y - z should be evaluated as (x - y) - z not x - (y-z)
		that is, other should be y, not (y-z).
		'''
		if isinstance(other, int) or isinstance(other, str):
			if isinstance(other, str):
				if len(other) == 0:
					other = 0
				elif len(other) == 1:
					other = ord(other)
				else:
					raise ValueError('cannot subtract string')
			if (other != 0):
				# could also add the negated value
				t = self.getResultType()
				if sizeInBits(t) == 16: # 'uint16' or t[-1] == '*':
					# check range
					checkRange(other, 16, isSigned(t)) # > 65535 or other < -32768):
					self.emit('MOV A, R2')
					self.emit('CLR C') # don't borrow
					self.emit('SUBB A, #0x%x', other & 0xff)
					self.emit('MOV R%d, A', 2)
					self.emit('MOV A, R3')
					self.emit('SUBB A, #0x%x', (other >> 8) & 0xff)
				elif sizeInBits(t) == 8: # assume 8-bit
					checkRange(other, 8, isSigned(t))
					self.emit('CLR C') # don't borrow
					self.emit('SUBB A, #0x%x', other)
					self.emit('MOV R%d, A', 3)
				else:
					raise TypeError('unsupported type %s in - operator' % t)
			# else, subtract 0, nothing to do
		elif isinstance(other, CodeCapsule):
			t1 = self.getResultType()
			t2 = other.getResultType()
			if sizeInBits(t1) == 8 and sizeInBits(t2) == 8:
				# for x - y, first generate code for y
				# do not generate code out of order
				temp = self.allocTemp()        # allocate temp for x
				self.saveAinTemp(temp)         # save x in temp
				self.appendCode(other)         # put code for y
				# now x is in temp, y is in A
				self.emit('XCH A, R%d', temp.varAddress()) #  (exchange) so x is in A, y is in temp
				self.emit('CLR C')  # don't borrow
				self.emit('SUBB A, R%d', temp.varAddress()) # now do A = A - Rn
				self.freeTemp(temp)
			else:
				if sizeInBits(t1) == 16 and sizeInBits(t2) == 16:
					# push R2 and R3 on stack
					self.emit('PUSH 0x%x', 3)
					self.emit('PUSH 0x%x', 2)
					self.appendCode(other)
					self.emit('POP ACC')
					self.emit('CLR C')
					self.emit('SUBB A, R%d', 2)
					self.emit('POP ACC')
					self.emit('SUBB A, R%d', 3)
				else:
					raise TypeError('mixed uint16 - uint8 not yet supported')
		else:
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __rsub__(self, other):
		'''
			sub is not commutative. this could be 1 - mcu.Reg
			so we evaluate mcu.Reg, load number into A, then 
			A = A - Reg
		'''
		if isinstance(other, int) or isinstance(other, str):
			if isinstance(other, str):
				if len(other) == 0:
					other = 0
				elif len(other) == 1:
					other = ord(other)
				else:
					raise ValueError('cannot rsub string')
			t = self.getResultType()
			if sizeInBits(t) == 8:
				checkRange(other, 8, isSigned(t))
				temp = self.allocTemp()
				self.saveAinTemp(temp)
				self.emit('MOV A, #0x%x', other)
				self.emit('SUBB A, R%d', temp.varAddress())
				self.freeTemp(temp)
			elif sizeInBits(t) == 16:
				checkRange(other, 16, isSigned(t))
				# handle 16-bit sub
				self.emit('MOV A, #0x%x', other & 0xff)
				self.emit('CLR C')
				self.emit('SUBB A, R%d', 2)
				self.emit('MOV R%d, A')
				self.emit('MOV A, #0x%x', (other >> 8) & 0xff)
				self.emit('SUBB A, R%d', 3)
				self.emit('MOV R%d, A', 3)

		else: # not handled
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __and__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 0 or other == False:
					self.emit('CLR C')
					# no need to set result type -- it is still bool
				elif other == 1 or other == True:
					pass
				else:
					raise ValueError('bitwise-and value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('bitwise-and type not bit: %s' % t2)
				# now generate code
				tempBit = self.allocTempBit() # allocate space for temporary
				self.saveCinTempBit(tempBit)  # save C into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('ANL C, 0x%x', tempBit.varAddress())
				self.freeTempBit(tempBit)
			else:
				raise ValueError('bitwise-and type unsupported: %s' % other)
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				if (other == 0):  # AND'ing 0 => always 0
					# check if self's type is a bool, uint8, uint16, ...
					self.emit('CLR A')
				elif ((other & 0xff) != 0xFF):
					# should we check range? 
					# should we limit it to 8 bits?
					self.emit('ANL A, #0x%x', other)
				# else, essentially a nop
				# else, skip.
				# no need to set the result type -- it is still uint8
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('bytewise-and type not byte: %s' % t2)
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				# OK to use register in this context
				self.emit('ANL A, R%d', temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types: %s and %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if isinstance(other, int):
				if other == 0:
					self.emit('CLR R%d', 2)
					self.emit('CLR R%d', 3)
				elif (other & 0xffff) != 0xffff:
					# can use only direct address rather than register in this mode
					self.emit('ANL 0x%x, #0x%x', 2, other & 0xff)
					self.emit('ANL 0x%x, #0x%x', 3, (other >> 8) & 0xff)
				# else it's a nop
			elif isinstance(other, CodeCapsule):
				# check if the other type is also 16-bit. 
				# we don't yet do type promotion or sign extension 
				t2 = other.getResultType()
				if sizeInBits(t2) == 16:
					# push R2 and R3 on stack
					self.emit('PUSH 0x%x', 3)
					self.emit('PUSH 0x%x', 2)
					self.appendCode(other)
					self.emit('POP ACC')
					self.emit('ANL 0x%x, A', 2) # this allows only direct address not Ri
					self.emit('POP ACC')
					self.emit('ANL 0x%x, A', 3) # this allows only direct address not Ri
		else:
			raise TypeError('unsupported type for and: %s' % t)
		return self

	def __rand__(self, other):  # This is commutative
		return self.__and__(other)

	def __or__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 1 or other == True:
					self.emit('SETB C')
					# no need to set result type -- it is still bool
				elif other == 0 or other == False:
					# essentially a nop
					pass
				else:
					raise ValueError('bitwise-or value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t = other.getResultType()
				if sizeInBits(t) != 1:
					raise TypeError('bitwise-or type not bit: %s' % t)
				# now generate code
				tempBit = self.allocTempBit()
				self.saveCinTempBit(tempBit)
				self.appendCode(other)
				self.emit('ORL C, %x', tempBit.varAddress())
				self.freeTempBit(tempBit)
			else:
				raise ValueError('bitwise-or type unsupported: %s' % type(other))
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				# should we check range?
				if (other == 0xff): # OR'ing ff => always ff
					self.emit('MOV A, #0x%x', 0xff)
				elif (other != 0):
					self.emit('ORL A, #0x%x', other)
				# else, essentially a nop
				# else, skip.
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('bytewise-or type not byte: %s' % t2)
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('ORL A, R%d', temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types: %s or %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if isinstance(other, int):
				checkRange(other, 16, isSigned(t))
				# can use only direct address in this context
				self.emit('ORL 0x%x, #0x%x', 2, other & 0xff)
				self.emit('ORL 0x%x, #0x%x', 3, (other >> 8) & 0xff)
			elif isinstance(other, codecapsule.CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) == 16: # maybe also allow pointer?
					self.emit('PUSH 0x%x', 3)
					self.emit('PUSH 0x%x', 2)
					self.appendCode(other)
					self.emit('POP ACC')
					self.emit('ORL 0x%x, A', 2) # this allows only direct address not Ri
					self.emit('POP ACC')
					self.emit('ORL 0x%x, A', 3) # this allows only direct address not Ri
		else:
			raise TypeError('unsupported type for or: %s' % t)
		return self

	def __ror__(self, other):
		return self.__or__(other)

	def __xor__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 0 or other == False:
					# we are XOR'ing with a 0 => it's a nop.
					pass
				elif other == 1 or other == True:
					# it's a complement
					self.emit('CPL C')
				else:
					raise ValueError('bitwise-xor value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('bitwise-xor type not bit: %s' % t2)
				# generate code
				# test if bit is 0 or 1. if 1, complement.
				tempBit = self.allocTempBit()
				self.saveCinTempBit(tempBit)
				self.appendCode(other)
				self.emit('JNB 0x%x, 0x%x', tempBit.varAddress(), 1)
				# if temp bit is 0 then skip the next instruction (1 byte)
				# if temp bit is 1 then complement C = other
				self.emit('CPL C')
				# in either case, fall through back to the same
			else:
				raise ValueError('bitwise-xor type unsupported: %s' % other)
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				# check range?
				if (other == 0): #nop
					pass
				elif other == 0xff:
					# same as complement
					self.emit('CPL A')
				else:
					self.emit('XRL A, #0x%x', other)
			elif isinstance(other, Capsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('bytewise-xor type not byte: %s' % t2)
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('XRL A, R%d', temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types: %s xor %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if isinstance(other, int):
				checkRange(other, 16, isSigned(t))
				self.emit('XRL 0x%x, #0x%x', 2, other & 0xff)
				self.emit('XRL 0x%x, #0x%x', 3, (other >> 8) & 0xff)
			elif isinstance(other, codecapsule.CodeCapsule):
				t2 = other.getResultType()
				if (sizeInBits(t2) == 16):
					# push R2 and R3 on stack
					self.emit('PUSH 0x%x', 3)
					self.emit('PUSH 0x%x', 2)
					self.appendCode(other)
					self.emit('POP ACC')
					self.emit('XRL 0x%x, A', 2)
					self.emit('POP ACC')
					self.emit('XRL 0x%x, A', 3)
		else:
			raise TypeError('unsupported type for xor: %s' % type(other))
		return self

	def __rxor__(self, other):
		'''reflected: given a + b, self = b, other = a.
		'''
		return self.__xor__(other)

	def __iadd__(self, other):
		'''this is the a += b. the implementation here is not quite right,
			 but it is just a placeholder for now. It is not too hard:
			 we need to remember the source variable (L-value) from the code capsule,
			 and write it back.
			 however, this gets complicated when the RHS is an indexing operator or
			 a "." operator; still doable.
		'''
		self.__add__(other)
		return self

	def __isub__(self, other):
		'''this is the a -= b. the implementation here is not quite right,
		   but it is just a placeholder for now.
		'''
		self.__sub__(other)
		return self

	def __iand__(self, other):
		'''iand &= is special because 8051 provides atomic instructions
		   but for now we don't support it yet...
			 we would need to go back to the source instead of loading it into A
		'''
		self.__and__(other)
		return self

	def __ior__(self, other):
		'''this is the a |= b. placeholder for now'''
		self.__or__(other)
		return self

	def __ixor__(self, other):
		'''this is the a ^= b. placeholder for now'''
		self.__xor__(other)
		return self

	def __imul__(self, other):
		'''this is the a *= b. placeholder for now'''
		self.__mul__(other)
		return self

	def __idiv__(self, other):
		'''this is a placeholder for a /= b. placeholder for now'''
		self.__div__(other)
		return self

	def __itruediv__(self, other):
		'''this is a placeholder for a //= b. placeholder for now.'''
		self.__truediv__(other)
		return self

	def __imod__(self, other):
		self.__mod__(other)
		return self


	def __invert__(self):
		'''this is the bit-invert operator'''
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# just complement C
			'''I think in SDCC, ~ on a boolean gets promoted to a byte??'''
			self.emit('CPL C')
		elif sizeInBits(t) == 8:
			# complement the byte
			self.emit('CPL A')
		elif sizeInBits(t) == 16:
			# complement the R3:R2.
			# use XCH to preserve the value inside A
			self.emit('XCH A, R%d', 3)
			self.emit('CPL A')
			self.emit('XCH A, R%d', 3)
			self.emit('XCH A, R%d', 2)
			self.emit('CPL A')
			self.emit('XCH A, R%d', 2)
		else:
			raise TypeError("invert operator not supported for %s type" % t)
		return self

	def __neg__(self):
		'''this is the unary negation operator. we take two's complement.
		   some possibilities: negate and promote uint8 (and uint16?) to signed int?
			 what happens to overflow?
		'''
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# we have the option of negating it or promote to int before negating
			# for now, let me just complement the bit, even though I think it is
			# useful to mimic the C ! operator (python's not, which can't be
			# overridden
			self.emit('CPL C')
		elif sizeInBits(t) == 8:
			# simply take 2's complement
			self.emit('CPL A')
			self.emit('INC A')
		elif sizeInBits(t) == 16:
			# take 2's complement on lower byte
			self.emit('XCH A, R%d', 2)  # swap R2 with A because need to do it in A
			self.emit('CPL A')   # 1's complement
			self.emit('INC A')   # plus 1
			self.emit('XCH A, R%d', 2)  # swap A back into R2
			self.emit('XCH A, R%d', 3)  # swap R3 into A
			# do the subtract with borrow trick!
			self.emit('SUBB A, #0x%x', 0) # (upper - C)
			self.emit('CPL A') # ~(upper - C) = -(upper - C) - 1 
						# = -upper + C - 1 = ~upper+1 + C - 1 = ~upper + C
			self.emit('XCH A, R%d', 3)  # put upper byte back into R3
		return self


	# other operators include
	# __ipow__(self, other)
	# __ilshift__(self, other)
	# __irshift__(self, other)
	# __iand__(self, other)
	# __ixor__(self, other)
	# __ior__(self, other)

	# __pos__(self)
	# __abs__(self)
	# __complex__(self)
	# __int__(self)
	# __long__(self)
	# __float__(self)


	def __eq__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 1 or other == True:
					# want to check if self (bool) == 1.
					# nothing to do!
					# no need to set result type -- it is still bool
					pass
				elif other == 0 or other == False:
					# want to check if self (bool, C) == 0.
					# simply complement C.
					self.emit('CPL C')
				else:
					# well.. we could do a promotion of bit to int?
					raise ValueError('== value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('== type not bit: %s' % t2)
				# now generate code. count # of bits
				tempBit = self.allocTempBit()
				self.saveCinTempBit(tempBit)
				self.appendCode(other)
				self.emit('CLR A')
				self.emit('JNC 0x%x', 1)
				self.emit('INC A')
				self.emit('JB 0x%x, 0x%x', tempBit.varAddress(), 1)
				self.freeTempBit(tempBit)
				self.emit('INC A')
				# A now contains a + !b.
				# 1 + !1 = 1 or 0 + !0 = 1.
				# so, rotate A.0 back into C for equality.
				self.emit('RRC A')
			else:
				raise ValueError('equality type unsupported: %s' % other)
		elif sizeInBits(t) == 8:
			if isinstance(other, int) or isinstance(other, str):
				if isinstance(other, str):
					if len(other) == 0:
						other = 0
					elif len(other) == 1:
						other = ord(other)
					else:
						raise ValueError('cannot compare 8-bit with string literal')
				# compare and jump if not equal
				checkRange(other, 8, isSigned(other))
				self.emit('CLR C')
				self.emit('XRL A, #0x%x', other) 
				self.emit('JNZ 0x%x', 1) # if not equal, skip
				self.emit('SETB C') # equal => set C to 1
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then compare
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('%s == type not byte: %s' % (t, t2))
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('CLR C') # assume not equal
				self.emit('XRL A, R%d', temp.varAddress())
				self.emit('JNZ 0x%x', 1) # if not equal, skip to keep C=0
				self.emit('SETB C') # equal => set C to 1
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types for equality comparison: %s == %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if (isinstance(other, int)):
				# compare with int literal
				self.emit('CLR C') # assume not equal
				self.emit('MOV A, R2')
				self.emit('XRL A, #0x%x', other & 0xff) # compare lower byte
				self.emit('JNZ 0x%x', 5) # if not equal, skip
				self.emit('MOV A, R3') # this is 1 byte
				self.emit('XRL A, #0x%x', (other >> 8) & 0xff) # 2 bytes
				self.emit('JNZ 0x%x', 1) # if not equal, skip # 1 byte
				self.emit('SETB C') # otherwise, equal, set to 1. # 1 byte
			elif isinstance(other, CodeCapsule):
				# compare two 16-bit expressions
				self.emit('PUSH 0x%x', 3)
				self.emit('PUSH 0x%x', 2)
				self.appendCode(other)
				self.emit('POP ACC')
				# subtract lower byte.
				self.emit('CLR C')  # this clears C bit for subtract
				self.emit('XRL 0x%x, A', 2) # R2 = R2 xor lower byte
				self.emit('POP ACC')  # get self's lower byte
				self.emit('XRL A, R%d', 2)  # if R2 had better be 0 to preserve A
				self.emit('XRL A, R%d', 3)  # finally compare upper bytes
				self.emit('JNZ 0x%x', 1) # if not equal, skip 1 byte
				self.emit('SETB C')  # set C = 1 if equal.
		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for ==: %s' % t)
		self.setResultType('bool')
		return self

	def __ne__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 0 or other == False:
					# want to check if self (bool) != 1.
					# nothing to do!
					# no need to set result type -- it is still bool
					pass
				elif other == 1 or other == True:
					# want to check if self (bool, C) != 0.
					# simply complement C.
					self.emit('CPL C')
				else:
					raise ValueError('!= value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('!= type not bit: %s' % t2)
				# now generate code. count # of bits
				tempBit = self.allocTempBit()
				self.saveCinTempBit(tempBit)
				self.appendCode(other)
				self.emit('CLR A')
				self.emit('JNC 0x%x', 1)
				self.emit('INC A')
				self.emit('JNB 0x%x, 0x%x', tempBit.varAddress(), 1)
				self.freeTempBit(tempBit)
				self.emit('INC A')
				# A now contains a + b.
				# 1 + 0 = 1 or 0 + 1 = 1.
				# so, rotate A.0 back into C for equality.
				self.emit('RRC A')
			else:
				raise ValueError('!= type unsupported: %s' % other)
		elif sizeInBits(t) == 8:
			if isinstance(other, int) or isinstance(other, str):
				# compare and jump if not equal
				if isinstance(other, str):
					if len(other) == 0:
						other = 0
					elif len(other) == 1:
						other = ord(other)
					else:
						raise ValueError('cannot compare 8-bit with string literal')
				self.emit('SETB C') # assume not equal
				self.emit('XRL A, #0x%x', other)
				self.emit('JNZ 0x%x', 1)  # if not equal, keep C=1
				self.emit('CLR C') # equal => set C to 0
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('!= type not byte: %s' % t2)
					# we don't yet support type promotion from 8 bit to 16 bit
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				self.emit('SETB C') # assume not equal
				self.emit('XRL A, 0x%x', temp.varAddress()) # compare other with this
				self.emit('JNZ 0x%x', 1) # if not equal, skip and keep C=1
				self.emit('CLR C') # equal => set C to 0
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types for inequality comparison: %s != %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			# opposite of equality comparison
			if (isinstance(other, int)):
				# compare with int literal
				self.emit('SETB C') # assume not equal
				self.emit('MOV A, R2')
				self.emit('XRL A, #0x%x', other & 0xff)
				self.emit('JNZ 0x%x', 5) # if not equal, skip clearing
				self.emit('MOV A, R3') # grab upper byte
				self.emit('XRL A, #0x%x', (other >> 8) & 0xff)
				self.emit('JNZ 0x%x', 1) # if not equal, skip clearing
				self.emit('CLR C')  # otherwise, equal, set to 0.
		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for !=: %s' % t)
		self.setResultType('bool')
		return self

	def __lt__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# strictly speaking, can't compare boolean.
			raise TypeError('< cannot compare boolean')
		elif sizeInBits(t) == 8:
			if isinstance(other, int) or isinstance(other, str):
				if isinstance(other, str):
					if len(other) == 0:
						other = 0
					elif len(other) == 1:
						other = ord(other)
					else:
						raise ValueError('cannot compare 8-bit with string literal')
				# x - y. if negative then x < y
				self.emit('CLR C') # don't borrow
				self.emit('SUBB A, #0x%x', other)
				self.emit('RLC A') # rotate sign bit into C
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('< type not byte: %s' % t2)
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				# swap A and temp reg back into correct order
				self.emit('XCH A, R%d', temp.varAddress())
				self.emit('CLR C') # don't borrow
				# subtract and rotate the sign bit back into C
				self.emit('SUBB A, R%d', temp.varAddress())
				self.freeTemp(temp)
				self.emit('RLC A')
			else:
				raise TypeError('incompatible types for %s < %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if (isinstance(other, int)):
				# do subtract. Essentially sign bit
				self.emit('CLR C')
				self.emit('MOV A, R2')
				self.emit('SUBB A, #0x%x', other & 0xff)
				self.emit('MOV A, R3')
				self.emit('SUBB A, #0x%x', (other >> 8) & 0xff)
				self.emit('RLC A') # rotate sign bit into C
			elif isinstance(other, codecapsule.CodeCapsule):
				# subtract and do the same rotate
				self.emit('PUSH 0x%x', 3)
				self.emit('PUSH 0x%x', 2)
				self.appendCode(other)
				self.emit('POP ACC')
				self.emit('CLR C')
				self.emit('SUBB A, R%d', 2)
				self.emit('POP ACC')
				self.emit('SUBB A, R%d', 2)
				self.emit('RLC A')
		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for <: %s' % t)
		self.setResultType('bool')
		return self


	def __le__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# strictly speaking, can't compare boolean.
			raise TypeError('<= cannot compare boolean')
		elif sizeInBits(t) == 8:
			if isinstance(other, int) or isinstance(other, str):
				if isinstance(other, str):
					if len(other) == 0:
						other = 0
					elif len(other) == 1:
						other = ord(other)
					else:
						raise ValueError('cannot compare 8-bit with string literal')
				# x - y. if sign bit = 1 or A = 0 then x <= y
				self.emit('CLR C') # don't borrow
				self.emit('SUBB A, #0x%x', other)
				self.emit('JNZ 0x%x', 1)  # if A != 0, skip 1 instruction
				# if zero then hack by forcing sign bit into A
				self.emit('CPL A') # was 0, now 0xff
				self.emit('RLC A') # rotate sign bit into C
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('<= type not byte: %s' % t2)
				temp = self.allocTemp() # allocate space for temporary
				self.saveAinTemp(temp)  # save A into temporary
				self.appendCode(other)  # take code already generated,
				# don't swap -- do y - x and complement sign bit
				self.emit('CLR C') # don't borrow
				self.emit('SUBB A, R%d', temp.varAddress())
				self.freeTemp(temp)
				# the sign bit back into C
				self.emit('RLC A')
				# sign = 1 means y < x, so !sign means y >= x
				self.emit('CPL C')
			else:
				raise TypeError('incompatible types for %s <= %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			# subtract. y - x and complement sign bit.
			if isintanceof(other, int):
				self.emit('CLR C')
				self.emit('MOV A, R2')
				self.emit('SUBB A, #0x%x', other & 0xff)
				self.emit('MOV A, R3')
				self.emit('SUBB A, #0x%x', (other >> 8) & 0xff)
				self.emit('RLC A')
				self.emit('CPL C')

		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for <=: %s' % t)
		self.setResultType('bool')
		return self

	def __ge__(self, other):
		'''This is essentially the same as __lt__ except it complements the C bit
		'''
		t = self.getResultType()
		if sizeInBits(t) == 1:
			raise TypeError('>= cannot compare boolean')
		elif sizeInBits(t) == 8:
			if isinstance(other, int) or isinstance(other, str):
				if isinstance(other, str):
					if len(other) == 0:
						other = 0
					elif len(other) == 1:
						other = ord(other)
					else:
						raise ValueError('cannot compare 8-bit with string literal')
				# x - y < 0.  if negative then x < y; otherwise x >= y
				self.emit('CLR C')
				self.emit('SUBB A, #0x%x', other)
				self.emit('RLC A')
				self.emit('CPL C')
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('>= type not byte: %s' % t2)
				temp = self.allocTemp()
				self.saveAinTemp(temp)
				self.appendCode(other)
				self.emit('XCH A, R%d', temp.varAddress())
				self.emit('CLR C')
				self.emit('SUBB A, R%d', temp.varAddress())
				self.freeTemp(temp)
				self.emit('RLC A')
				self.emit('CPL C')
			else:
				raise TypeError('incompatible types for %s >= %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if (isinstance(other, int)):
				self.emit('CLR C')
				self.emit('MOV A, R2')
				self.emit('SUBB A, #0x%x', other & 0xff)
				self.emit('MOV A, R3')
				self.emit('SUBB A, #0x%x', (other >> 8) & 0xff)
				self.emit('RLC A')
				self.emit('CPL C')
			elif isinstance(other, codecapsule.CodeCapsule):
				# subtract and do the same rotate
				self.emit('PUSH 0x%x', 3)
				self.emit('PUSH 0x%x', 2)
				self.appendCode(other)
				self.emit('POP ACC')
				self.emit('CLR C')
				self.emit('SUBB A, R%d', 2)
				self.emit('POP ACC')
				self.emit('SUBB A, R%d', 2)
				self.emit('RLC A')
				self.emit('CPL C')
		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for >=: %s' % t)
		self.setResultType('bool')
		return self




	def __gt__(self, other):
		pass

	def __mul__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# can't multiply boolean. but maybe we allow it as AND?
			raise TypeError("can't multiply boolean")
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				# check range?
				checkRange(other, 8, isSigned(t))
				# now use the MUL AB operator
				self.emit('MOV B, #0x%x', other) # this is the second operand
				# now restore the first operand into A
				self.emit('MUL AB')
				# now put the result into R3:R2
				self.emit('MOV R%d, A', 2)
				self.emit('MOV R%d, B', 3)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) == 8:
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.appendCode(other)
					self.emit('MOV B, A') # this is the second operand
					self.emit('MOV A, R%d', temp.varAddress())  # restore the first operand
					self.freeTemp(temp)
					self.emit('MUL AB')
					self.emit('MOV R%d, A', 2)
					self.emit('MOV R%d, B', 3)
				else:
					raise TypeError('multiplying other %s unsupported' % other)
				self.setResultType('uint16')
		else:
			raise TypeError('Multiplying %s unsupported' % t)
		return self

	def __div__(self, other):
		pass

	def __truediv__(self, other):
		pass

	def __floordiv__(self, other):
		pass

	def __mod__(self, other):
		pass

	def __divmod__(self, other):
		pass

	def __pow__(self, other, mod):
		pass

	def __lshift__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 8:
			if isinstance(other, int):
				# fixed number of positions
				# let's try it for each case.
				if other == 0:
					pass # nothing to do when you shift by 0
				elif other == 1:
					# rotate left and clear last bit
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFE) # clear last bit
				elif other == 2:
					self.emit('RL A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFC) # clear last two bits
				elif other == 3:
					# swap lower and upper nibbles and then rotate right, and clear
					self.emit('SWAP A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xF8) # clear the last 3 bits
				elif other == 4:
					self.emit('SWAP A')
					self.emit('ANL A, #0x%x', 0xF0) # clear the last 4 bits
				elif other == 5:
					self.emit('SWAP A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xE0) # clear the last 5 bits
				elif other == 6: # same as rotating right twice and mask
					self.emit('RR A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xC0) 
				elif other == 7: # same as rotating right once and mask
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x80)
				elif other >= 8: # just set to 0
					self.emit('CLR A')
				elif other < 0:
					raise ValueError('Does not support shift by negative positions')
			# elif isinstance(other, CodeCapsule):
				# this is a little harder... we need to allocate a counter variable
				# and use a loop, right?
			else:
				raise TypeError('Left shift does not yet support variable # of positions')
		elif sizeInBits(t) == 16: # should not rotate pointers...
			if isinstance(other, int):
				# shift 16 bits left by a fixed number of positions.
				# we rotate but put the bits into upper before masking out.
				if other == 0:
					pass
				elif other == 1:
					# Strategy: rotate lower-byte high-bit into C using RLC,
					# then RLC into higher byte.
					self.emit('MOV A, R3')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFE)
					self.emit('MOV R%d, A', 3)
					self.emit('MOV A, R2')
					self.emit('CLR C')
					self.emit('RLC A')
					self.emit('ANL A, #0x%x', 0xFE)
					self.emit('MOV R%d, A', 2)
					self.emit('MOV A, R3')
					self.emit('RLC A')
					self.emit('MOV R%d, A', 3)
				elif other == 2:
					# rotate lower, save lower bits, rotate upper, OR in bits
					self.emit('MOV A, R2')
					self.emit('RL A')
					self.emit('RL A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.emit('ANL A, #0x%x', 0xFC) # clear last two bits
					self.emit('MOV R%d, A', 2)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0x3)
					# now rotate the upper byte
					self.emit('MOV A, R3')  # load it into A
					self.emit('RL A')  # rotate twice
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFC)  # clear out lower bit
					self.emit('ORL A, R%d', temp.varAddress())  # Combining two bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 3) # put the result back into R3
				elif other == 3:
					# swap and rotate right
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					self.emit('RR A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.emit('ANL A, #0x%x', 0xF8) # clear last three bits
					self.emit('MOV R%d, A', 2)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0x7) # extract 3 bits
					# to be shifted from lower byte to upper byte, keep it in temp.
					# now rotate the upper byte
					self.emit('MOV A, R3')  # load it into A
					self.emit('SWAP A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xF8)  # clear out lower 3 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 3 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 3) # put the result back into R3
				elif other == 4:
					# swap and rotate right
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.emit('ANL A, #0x%x', 0xF0) # clear last 4 bits
					self.emit('MOV R%d, A', 2)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xF) # extract 4 bits
					# to be shifted from lower byte to upper byte, keep it in temp.
					# now rotate the upper byte
					self.emit('MOV A, R3')  # load it into A
					self.emit('SWAP A')
					self.emit('ANL A, #0x%x', 0xF0)  # clear out lower 4 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 4 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 3) # put the result back into R3
				elif other == 5:
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					self.emit('RL A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.emit('ANL A, #0x%x', 0xE0) # clear last 5 bits
					self.emit('MOV R%d, A', 2)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0x1F) # extract 5 bits
					# to be shifted from lower byte to upper byte, keep it in temp.
					# now rotate the upper byte
					self.emit('MOV A, R3')  # load it into A
					self.emit('SWAP A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xE0)  # clear out lower 5 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 4 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 3) # put the result back into R3
				elif other == 6:
					self.emit('MOV A, R2')
					self.emit('RR A')
					self.emit('RR A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					self.emit('ANL A, #0x%x', 0xC0) # clear last 6 bits
					self.emit('MOV R%d, A', 2)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0x3F) # extract 6 bits 
					# now rotate the upper byte
					self.emit('MOV A, R3')  # load it into A
					self.emit('RR A')  # rotate twice
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xC0)  # clear out lower 6 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 6 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 3) # put the result back into R3
				elif other == 7:
					self.emit('MOV A, R3') # rotate upper byte into C
					self.emit('RRC A')
					self.emit('MOV A, R2') # bring in lower byte
					self.emit('RRC A') # this makes high-order LSb now high-order MSb,
					# while OR'ing low-order <7:1>.  This forms the new high-order byte.
					self.emit('MOV R%d, A', 3)
					# now, take LSb of low-order byte and move it to high-order.
					self.emit('MOV A, R2')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x80)
					# now save it back
					self.emit('MOV R%d, A', 2)
				elif other == 8:
					# simple: replace higher byte with lower, clear out lower byte
					self.emit('CLR A')
					self.emit('XCH A, R2')  # A = old R2, R2 = 0
					self.emit('MOV R%d, A', 3)  # R3 = old R2
				elif other == 9:
					# like lowerByte << 1 except we write back into higherByte and clear
					# lowerByte
					self.emit('MOV A, R2')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFE)
					self.emit('MOV R%d, A', 3)        # R3 = R2 << 1
					self.emit('MOV R%d, #0x%x', 2, 0) # R2 = 0
				elif other == 10:
					self.emit('MOV A, R2')
					self.emit('RL A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xFC)
					self.emit('MOV R%d, A', 3)        # R3 = R2 << 2
					self.emit('MOV R%d, #0x%x', 2, 0) # R2 = 0
				elif other == 11:
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xF8)  # clear last 3 bits
					self.emit('MOV R%d, A', 3)      # R3 = R2 << 3
					self.emit('MOV R%d, #0x%x', 2, 0)  # R2 = 0
				elif other == 12:
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					self.emit('ANL A, #0x%x', 0xF0) # clear last 4 bits
					self.emit('MOV R%d, A', 3)     # R3 = R2 << 4
					self.emit('MOV R%d, #0x%x', 2, 0)  # R2 = 0
				elif other == 13:
					self.emit('MOV A, R2')
					self.emit('SWAP A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0xE0) # clear last 5 bits
					self.emit('MOV R%d, A', 3)       # R3 = R2 << 5
					self.emit('MOV R%d, #0x%x', 2, 0) # R2 = 0
				elif other == 14:
					self.emit('MOV A, R2')
					self.emit('RR A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0xC0)  # clear last 6 bits
					self.emit('MOV R%d, A', 3)        # R3 = R2 << 6
					self.emit('MOV R%d, #0x%x', 2, 0) # R2 = 0
				elif other == 15:
					self.emit('MOV A, R2')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x80)
					self.emit('MOV R%d, A', 3)
					self.emit('MOV R%d, #0x%x', 2, 0)
				elif other >= 16:
					# simply clear both registers
					self.emit('CLR A')
					self.emit('MOV R%d, A', 2)
					self.emit('MOV R%d, A', 3)
			else:
				raise ValueError('left-shift cannot handle variable positions yet')
		return self

	def __rshift__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 8:
			if isinstance(other, int):
				# fixed number of positions
				# let's try it for each case.
				if other == 0:
					pass # nothing to do when you shift by 0
				elif other == 1:
					# save sign bit if it is signed byte.
					if (isSigned(t)): # signed => copy sign bit
						self.emit('MOV C, ACC.%d', 7)
					else:  # unsigned => fill in 0
						self.emit('CLR C')
					# rotate right
					self.emit('RRC A')
				elif other == 2:
					if (isSigned(t)): # save sign bit
						self.emit('MOV C, ACC.%d', 7)
					else:
						self.emit('CLR C')
					self.emit('RRC A')
					# do it again
					if (isSigned(t)):
						self.emit('MOV C, ACC.%d', 7)
					else:
						self.emit('CLR C')
					self.emit('RRC A')
				elif other == 3:
					# swap lower and upper nibbles and then rotate right, and clear
					self.emit('SWAP A')
					self.emit('RL A')
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 4, 4) # if sign bit is set, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xE0) # set the upper 3 bits
						self.emit('SJMP 0x%x', 2)
					self.emit('ANL A, #0x%x', 0x1F) # clear the upper 3 bits
				elif other == 4:
					self.emit('SWAP A')
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 3, 4) # if sign bit is set, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF0) # set the top 4 bits
						self.emit('SJMP 0x%x', 2)
					self.emit('ANL A, #0x%x', 0x0F) # clear the top 4 bits
				elif other == 5:
					self.emit('SWAP A')
					self.emit('RR A')
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 2, 4) # if sign bit is set, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF8) # set the top 5 bits
						self.emit('SJMP 0x%x', 2)
					self.emit('ANL A, #0x%x', 0x07) # clear the top 5 bits
				elif other == 6: # same as rotating right twice and mask
					self.emit('RL A')
					self.emit('RL A')
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 1, 4) # if sign bit is not set, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xFC) # set the top 6 bits
						self.emit('SJMP 0x%x', 2)
					self.emit('ANL A, #0x%x', 0x03)  # clear top 6 bits
				elif other == 7: # same as rotating right once and mask
					self.emit('RLC A') # put sign bit
					self.emit('CLR A')
					if (isSigned(t)):
						self.emit('JNC 0x%x', 1) # if C is false, skip 1 byte
						self.emit('CPL A')       # if C true, make it 0xff.
					else:
						self.emit('RLC A')
					# 3 possible outcomes: if C is 0 => 0 no matter what.
					# if signed:  C => 0xff; if unsigned, C => 0x1.
					# we could use ADDC
					self.emit('ANL A, #0x%x', 0x80)
				elif other >= 8:
					if (isSigned(t)):
						self.emit('RLC A') # save sign bit
						# the only possible outcome is 0 or 1, depending on C.
						self.emit('CLR A')
						self.emit('JNC 0x%x', 1) # if C false, skip 1 byte
						self.emit('CPL A')       # if C true, make it 0xff
					else: # unsigned => just set to 0
						self.emit('CLR A')
				elif other < 0:
					raise ValueError('Does not support shift by negative positions')
			# elif isinstance(other, CodeCapsule):
				# this is a little harder... we need to allocate a counter variable
				# and use a loop, right?
			else:
				raise TypeError('Left shift does not yet support variable # of positions')
		elif sizeInBits(t) == 16: # should not rotate pointers...
			if isinstance(other, int):
				# shift 16 bits left by a fixed number of positions.
				# we rotate but put the bits into upper before masking out.
				if other == 0:
					pass
				elif other == 1:
					# Strategy: rotate lower-byte high-bit into C using RRC,
					# then RLC into higher byte.
					self.emit('MOV A, R3')
					if (isSigned(t)):
						self.emit('MOV C, ACC.%d', 7)
					else:
						self.emit('CLR C')
					self.emit('RRC A')  # move bit 8 into C
					self.emit('MOV R%d, A', 3)
					self.emit('MOV A, R2')
					self.emit('RRC A')  # rotate bit 8 (from upper byte) into bit 7 (of lower byte)
					self.emit('MOV R%d, A', 2)
				elif other == 2:
					# rotate higher, save new higher bits for lower byte, rotate lower, OR in bits
					self.emit('MOV A, R3')
					self.emit('RR A')
					self.emit('RR A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 6, 4) # skip next 4 bytes if signed bit is 0
						self.emit('ORL A, #0x%x', 0xC0)  # sign extend
						self.emit('SJMP 0x%x', 2)
					self.emit('ANL A, #0x%x', 0x3F) # clear upper two bits
					self.emit('MOV R%d, A', 3)      # finish upper byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xC0)
					# now rotate the upper byte
					self.emit('MOV A, R2')  # load it into A
					self.emit('RR A')  # rotate twice
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x3F)  # clear out upper 2 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining two bits from upper
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 2) # put the result back into R2
				elif other == 3:
					# swap and rotate right
					self.emit('MOV A, R3')
					self.emit('SWAP A')
					self.emit('RL A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 4, 4) # if signed bit is 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xE0)  # if sign-extend, OR in upper 3 bits
						self.emit('SJMP 0x%x', 2)        # skip 2 bytes
					self.emit('ANL A, #0x%x', 0x1F) # clear upper three bits
					self.emit('MOV R%d, A', 3)      # finish upper byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xE0) # extract 3 bits
					# to be shifted from higher byte to lower byte, keep it in temp.
					# now rotate the lower byte
					self.emit('MOV A, R2')  # load it into A
					self.emit('SWAP A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0x1F)  # clear out upper 3 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 3 bits from upper
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 2) # put the result back into R2
				elif other == 4:
					# swap and rotate right
					self.emit('MOV A, R3')
					self.emit('SWAP A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 3, 4) # if signed bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF0)  # sign extend
						self.emit('SJMP 0x%x', 2)  # skip 2 bytes
					self.emit('ANL A, #0x%x', 0x0F) # clear upper 4 bits
					self.emit('MOV R%d, A', 3)      # finish lower byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xF0) # extract 4 bits
					# to be shifted from upper byte to lower byte, keep it in temp.
					# now rotate the upper byte
					self.emit('MOV A, R2')  # load it into A
					self.emit('SWAP A')
					self.emit('ANL A, #0x%x', 0x0F)  # clear out upper 4 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 4 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 2) # put the result back into R3
				elif other == 5:
					self.emit('MOV A, R3')
					self.emit('SWAP A')
					self.emit('RR A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 2, 4) # if signed bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF8)  # fill upper 5 bits
						self.emit('SJMP 0x%x', 2)  # skip 2 bytes
					self.emit('ANL A, #0x%x', 0x07) # clear upper 5 bits
					self.emit('MOV R%d, A', 2)      # finish upper byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xF8) # extract 5 bits
					# to be shifted from lower byte to upper byte, keep it in temp.
					# now rotate the upper byte
					self.emit('MOV A, R2')  # load it into A
					self.emit('SWAP A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x0E)   # clear out upper 5 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 5 bits from upper
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 2) # put the result back into R2
				elif other == 6:
					self.emit('MOV A, R3')
					self.emit('RL A')
					self.emit('RL A')
					temp = self.allocTemp()
					self.saveAinTemp(temp)
					if (isSigned(t)):
						self.emit('JNB ACC.%d, 0x%x', 1, 4) # if signed bit not set, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xFC) # sign extend 6 bits
						self.emit('SJMP 0x%x', 2) # skip 2 bytes
					self.emit('ANL A, #0x%x', 0x3F) # clear upper 6 bits
					self.emit('MOV R%d, A', 3)      # finish upper byte
					self.emit('ANL 0x%x, #0x%x', temp.varAddress(), 0xFC) # extract 6 bits 
					# now rotate the lower byte
					self.emit('MOV A, R2')  # load it into A
					self.emit('RL A')  # rotate twice
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0x03)  # clear out upper 6 bits
					self.emit('ORL A, R%d', temp.varAddress())  # Combining 6 bits from lower
					self.freeTemp(temp)
					self.emit('MOV R%d, A', 2) # put the result back into R3
				elif other == 7:
					self.emit('MOV A, R2')  # bring in lower byte
					self.emit('RLC A')      # save the most-significant bit of lower byte into C
					self.emit('MOV A, R3') # bring in higher byte
					self.emit('RLC A') # this makes new lower byte, C now has old sign bit
					self.emit('MOV R%d, A', 2)  # write back to lower byte
					self.emit('CLR A')
					if isSigned(t):
						self.emit('JNC 0x%x', 1) # if not carry, skip 2 bytes
						self.emit('CPL A') # sign extend => make all 1s
					self.emit('MOV R%d, A', 3)
				elif other == 8:
					# simple: replace lower byte with higher, clear out higher byte,
					# then sign extend if necessary.
					self.emit('CLR A')
					self.emit('XCH A, R3')  # A = old R3, R3 = 0
					self.emit('MOV R%d, A', 2) # R2 = R3
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 7, 1) # if old sign bit is 0, skip 1 byte
						self.emit('CPL A') # sign extend => make upper byte all 1s
				elif other == 9:
					# like lowerByte << 1 except we write back into higherByte and clear
					# lowerByte
					self.emit('CLR A')
					self.emit('XCH A, R3')  # A = old R3, R3 = 0
					if isSigned(t):
						self.emit('MOV C, ACC.%d', 7)
					else:
						self.emit('CLR C')
					self.emit('RRC')  # this is upper >> 1
					self.emit('MOV R%d, A', 2)  # save into R2
					# upper byte should be either 0 extended or sign extended.
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 2) # if sign bit 0, skip 3 bytes
						self.emit('R3, #0x%x', 0xff)  # if sign bit, sign-extend upper byte
				elif other == 10:
					self.emit('CLR A')
					self.emit('XCH A, R3')  # A = old R3, R3 = 0
					self.emit('RR A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x3F) # clear top 2 bits
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 5, 4) # if sign bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xC0)  # sign extend - set upper 2 bits
						self.emit('MOV R3, #0x%x', 0xff)  # if sign bit, sign-extend upper byte
					self.emit('MOV R%d, A', 2)        # R2 = R3 >> 2
				elif other == 11:
					self.emit('CLR A')
					self.emit('XCH A, R3')
					self.emit('SWAP A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0x1F)  # clear top 3 bits
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 4, 4) # if sign bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xE0) # sign extend - set upper 3 bits
						self.emit('MOV R3, #0x%x', 0xff) # if sign bit, sign extend upper byte
					self.emit('MOV R%d, A', 2)      # R2 = R3 >> 3
				elif other == 12:
					self.emit('CLR A')
					self.emit('XCH A, R3')
					self.emit('SWAP A')
					self.emit('ANL A, #0x%x', 0x0F) # clear upper 4 bits
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 3, 4) # is sign bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF0) # sign extend upper 4 bits
						self.emit('MOV R3, #0x%x', 0xFF) # if sign bit, sign extend upper byte
					self.emit('MOV R%d, A', 2)     # R2 = R3 >> 4
				elif other == 13:
					self.emit('CLR A')
					self.emit('XCH A, R3')
					self.emit('SWAP A')
					self.emit('RR A')
					self.emit('ANL A, #0x%x', 0x07) # clear upper 5 bits
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 2, 4) # if sign bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xF8) # sign extend upper 5 bits
						self.emit('MOV R3, #0x%x', 0xFF) # if sign bit, sign extend upper byte
					self.emit('MOV R%d, A', 2)       # R2 = R3 >> 5
				elif other == 14:
					self.emit('CLR A')
					self.emit('XCH A, R3')
					self.emit('RL A')
					self.emit('RL A')
					self.emit('ANL A, #0x%x', 0x03)  # clear upper 6 bits
					if isSigned(t):
						self.emit('JNB ACC.%d, 0x%x', 1, 4) # if sign bit 0, skip 4 bytes
						self.emit('ORL A, #0x%x', 0xFC) # sign extend upper 6 bits
						self.emit('MOV R3, #0x%x', 0xFF) # if sign bit, sign extend upper byte
					self.emit('MOV R%d, A', 2)        # R2 = R3 >> 6
				elif other == 15:
					self.emit('CLR A')
					self.emit('XCH A, R3')
					self.emit('RLC A') # move sign bit into C
					self.emit('CLR A')
					if isSigned(t):
						self.emit('JNC 0x%x', 2) # if sign bit 0, skip 2 bytes
						# now fill both lower and upper bytes with all 1s
						self.emit('CPL A')
						self.emit('MOV R3, A')
					else:
						# unsigned - leave R3 = 0, rotate C bit into least-significant bit
						self.emit('RLC A')
					self.emit('MOV R2, A')
				elif other >= 16:
					# simply clear both registers
					if isSigned(t):
						# test sign bit. if 1, fill all. else clear all.
						self.emit('MOV A, R3')
						self.emit('RLC A')  # put sign bit in C
						self.emit('CLR A')
						self.emit('JNC 0x%x', 1) # if sign bit 0, skip 1 byte
						self.emit('CPL A')       # if sign bit, value = 0xff
					else:
						self.emit('CLR A')       # if unsigned, value = 0
					self.emit('MOV R%d, A', 2) # in either case, fill lower and upper bytes
					self.emit('MOV R%d, A', 3)
			else:
				raise ValueError('right-shift cannot handle variable positions yet')
		return self

	def __getitem__(self, index):
		'''this is self[index]. This works on pointer type;
		   should we also have array type too?
			 To do: need a class for declaring a name as a pointer or array type.
		'''
		t = self.getResultType()
		if t[-1] == '*':
			if sizeInBits(t[:-1]) in [8, 16]:
				# i.e., it's a pointer type, and the pointed unit size is a byte or a short.
				# compute the resulting address and load byte.
				if isinstance(index, int): # constant offset
					if sizeInBits(t[:-1]) == 16:
							index = index << 1  # 2 bytes of offset per element
					self.emit('XCH A, DPL')
					self.emit('ADD A, #0x%x', index & 0xff)
					self.emit('XCH A, DPL')
					self.emit('XCH A, DPH')
					self.emit('ADDC A, #0x%x', (index >> 8) & 0xff)
					self.emit('XCH A, DPH')
					# now DPTR has the pointer to the byte
					self.emit('MOVX A, @DPTR') # load byte
				elif isinstance(index, CodeCapsule):
					t2 = index.getResultType()
					if sizeInBits(t2) == 16:
						# save the base pointer
						self.emit('PUSH 0x%x', 3)
						self.emit('PUSH 0x%x', 2)
						self.appendCode(index)
						# if 2 byte element, then shift index left
						if sizeInBits(t[:-1]) == 16:
							self.emit('CLR C')
							self.emit('XCH A, R2')
							self.emit('RLC')  # shift in 0, capture top bit; could also add R2 itself
							self.emit('XCH A, R2')  # put it back
							self.emit('XCH A, R3')
							self.emit('RLC')  # grab top bit from lower byte; could also do ADDC R3 itself
							self.emit('XCH A, R3') # put it back
						# this completes the index offset
						self.emit('POP ACC')  # pop lower byte into accumulator
						self.emit('ADD A, R%d', 2)
						self.emit('XCH A, DPL')
						self.emit('POP ACC')  # pop upper byte into accumulator
						self.emit('ADDC A, R%d', 3)
						self.emit('XCH A, DPH')
						self.emit('MOVX A, @DPTR')
					elif sizeInBits(t2) == 8:
						# for now, treat this as an unsigned index.
						# but to do it right, it should be either 0-extended if unsigned
						# or sign-extended if signed!!
						self.emit('PUSH 0x%x', 3)
						self.emit('PUSH 0x%x', 2)
						self.appendCode(index)  # evaluates index, puts in A
						if sizeInBits(t[:-1]) == 16:
							# double the index
							self.emit('CLR C')
							self.emit('RLC A')  # shift left, fill in 0 on the right
						self.emit('POP 0x%x', 2) # this is how we say POP R2
						self.emit('ADD A, R%d', 2)
						self.emit('XCH A, DPL')
						self.emit('POP 0x%x', 3) # this is how we say POP R3
						self.emit('ADDC A, R%d', 3)
						self.emit('XCH A, DPH')
						self.emit('MOVX A, @DPTR')
					else:
						raise TypeError('array index of type %s unsupported' % t2)
				else: # it could be slice!  we should try to support this... maybe?
					raise TypeError('array index expression %s unsupported' % index)
			# if processed correctly, set the type of indexed expression
			# (uint8* becomes just uint8)
			self.setResultType(t[:-1])
		else:
			# not supported
			raise TypeError('array/pointer type %s unsupported' % t)
		return self



	def __setitem__(self, index, value):
		'''this is self[index] = value.
		   we should evaluate RHS first;
			 then compute the index and then pointer for LHS,
			 and then do a store rather than a load.
			 should check if RHS and LHS have same type.
		'''
		if isinstance(value, int) or isinstance(value, str):
			if isinstance(value, str):
				if len(value) == 0:
					value = 0
				elif len(value) == 1:
					value = ord(value)
				else:
					raise ValueError('assignment of string to array not supported yet')
			# nothing to do on RHS
			# Is the following statement right? or should it be source type?
			# It would be easiest if an R-value is used here.
			tArray = self.getResultType()
			if tArray[-1] == '*' and sizeInBits(tArray[:-1]) in [8, 16]:
				# was: if tArray == 'uint8*' or tArray == 'uint16*':
				# check index
				if isinstance(index, int):
					# might want to do a range check on the index, if length is known
					self.emit('XCH A, R%d', 2)
					self.emit('ADD A, #0x%x', index % 0xff)
					self.emit('MOV DPL, A')
					self.emit('XCH A, R%d', 3)
					self.emit('ADDC A, #0x%x', (index >> 8) & 0xff)
					self.emit('MOV DPH, A')
					# DPTR now has the pointer
					# fall through to do the actual store.
				elif isinstance(index, CodeCapsule):
					tIndex = index.getResultType()
					if sizeInBits(tIndex) == 8:
						# treat index as unsigned; if signed, might sign-extend?
						# might check range dynamically?
						self.emit('PUSH 0x%x', 3)
						self.emit('PUSH 0x%x', 2)
						self.appendCode(index)
						self.emit('POP 0x%x', 2)
						self.emit('ADD A, R%d', 2)
						self.emit('MOV DPL, A')
						self.emit('POP 0x%x', 3)
						self.emit('ADDC A, R%d', 3)
						self.emit('MOV DPH, A')
						# now DPTR has the pointer. Fall through to store
					elif sizeInBits(tIndex) == 16:
						# do 16-bit arithmetic instead
						self.emit('PUSH 0x%x', 3)
						self.emit('PUSH 0x%x', 2)
						self.appendCode(index)
						self.emit('POP ACC')
						self.emit('ADD A, R%d', 2)
						self.emit('MOV DPL, A')
						self.emit('POP ACC')
						self.emit('ADDC A, R%d', 3)
						self.emit('MOV DPH, A')
						self.emit('MOVX @DPTR, A')
						# now DPTR has the pointer. Fall through to store.
					else:
						raise TypeError('index type %s unsupported' % tIndex)
					# should check the range of value
				self.emit('MOV A, #0x%x', value & 0xff)  # truncate top
				self.emit('MOVX @DPTR, A')  # do the actual store
				# strictly speaking, setitem has no return type... but we do this to allow
				# cascaded assignment.
				self.setResultType(tArray[:-1])
				print self 
				# This is necessary because python interpreter ignores the
				# return value!
				return self
			else:
				# other types of arrays not supported
				raise TypeError('array type %s unsupported' % tArray)
		elif isinstance(value, CodeCapsule):
			# need to figure out its type and check compatibility with array.
			# since evaluation order is value, index, DPTR, store,
			# we need to generate code using value's codecapsule, rather than self.
			tValue = value.getResultType() 
			if sizeInBits(tValue) == 8:
				tArray = self.getResultType() 
				if tArray[-1] == '*' and sizeInBits(tArray) in [8, 16]:
					# was: tArray == 'uint8*' or tArray == 'uint16*':
					# accept this for now
					if isinstance(index, int):
						# pointer is in R3:R2
						value.emit('PUSH ACC')  # save result on stack
						value.appendCode(self)  # add the code to generate the pointer in R3:R2
						value.emit('MOV A, R%d', 2)  # A = lower address
						value.emit('ADD A, #0x%x', index & 0xff)  # add constant index lower byte
						value.emit('MOV A, DPL') # put lower byte into DPL
						value.emit('MOV A, R%d', 3)  # R3 is don't care, A = upper address
						value.emit('ADDC A, #0x%x', (index >> 8) & 0xff)
						value.emit('MOV A, DPH') # put higher byte into DPH
						value.emit('POP ACC')    # restore value into A
						value.emit('MOVX @DPTR, A') # write the (lower) data byte
						if sizeInBits(tArray[:-1]) == 16: # type pointed to is 2 bytes
							# clear out upper byte 
							value.emit('INC DPTR')
							value.emit('CLR A')
							value.emit('MOVX @DPTR, A') # clear out upper byte
						# this is necessary because Python shell ignores the return value!
						value.setResultType(tArray[:-1])
						print value 
						return value
					elif isinstance(index, CodeCapsule):
						tIndex = index.getResultType()
						if sizeInBits(tIndex) == 8:  # was == 'uint8':
							# save value on stack first
							value.emit('PUSH ACC')
							value.appendCode(index)
							# save index on stack also
							value.emit('PUSH ACC')
							# now code to evaluate pointer
							value.appendCode(self)
							value.emit('POP ACC')
							value.emit('ADD A, R%d', 2)
							value.emit('MOV DPL, A')
							value.emit('ADDC A, R%d', 3)
							value.emit('MOV DPH, A')
							value.emit('POP ACC')
							value.emit('MOVX @DPTR, A')
						# this is necessary because Python shell ignores the return value!
							value.setResultType(tArray[:-1])
							print value 
							return value
						elif sizeInBits(tIndex) == 16: # was 'uint16':
							value.emit('PUSH ACC')
							value.appendCode(index)
							value.emit('PUSH 0x%x', 3)
							value.emit('PUSH 0x%x', 2)
							value.appendCode(self)
							value.emit('POP ACC')
							value.emit('ADD A, R%d', 2)
							value.emit('MOV DPL, A')
							value.emit('POP ACC')
							value.emit('ADDC A, R%d', 3)
							value.emit('MOV DPH, A')
							value.emit('POP ACC')
							value.emit('MOVX @DPTR, A')
						# this is necessary because Python shell ignores the return value!
							value.setResultType(tArray[:-1])
							print value 
							return value
						else:
							raise TypeError('index type %s unsupported' % tIndex)
					else:
						raise TypeError('index %s unsupported' % index)
				else:
					raise TypeError('array/pointer type %s unsupported', tArray)
			else:
				raise TypeError('value type %s for array assignment unsupported', tValue)
		else:
			raise TypeError('value %s unsupported' % value)


