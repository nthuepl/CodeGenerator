# cc_avr.py
# this is code capsule for AVR instruction set
#
from codecapsule import CodeCapsule
from isa_avr import ISAAVR


typeDef = {
		'bool':           { 'size': 1,  'signed': False, 'align': False, },
		'char':           { 'size': 8,  'signed': True,  'align': False, },
		'unsigned char':  { 'size': 8,  'signed': False, 'align': False, },
		'char*':          { 'size': 32, 'signed': False, 'align': True, },
		'uint8':          { 'size': 8,  'signed': False, 'align': False, },
		'uint8*':         { 'size': 32, 'signed': False, 'align': True, },
		'int8':           { 'size': 8,  'signed': True,  'align': False, },
		'int8*':          { 'size': 32, 'signed': False, 'align': True, },
		'short':          { 'size': 16, 'signed': True,  'align': True },
		'unsigned short': { 'size': 16, 'signed': False, 'align': True },
		'uint16':         { 'size': 16, 'signed': False, 'align': True },
		'uint16*':        { 'size': 32, 'signed': False, 'align': True },
		'uint32':         { 'size': 32, 'signed': False, 'align': True },
		'uint32*':        { 'size': 32, 'signed': False, 'align': True },
		'int32':          { 'size': 32, 'signed': True, 'align': True },
		'int32*':         { 'size': 32, 'signed': False, 'align': True },
		}

def sizeInBits(typeName):
	#if not VAR._typeDef.has_key(typeName):
	#	raise TypeError('unknown type %s' % typeName)
	# look up number of bits
	if typeName[-1] == '*':
		return 16  # pointers are 16 bits, right?
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


class CC_AVR(CodeCapsule):
	'''This is the code capsule class for the AVR ISA.
	   It inherits the generic structure of CodeCapsule class and
		 provides the common code for the interactive code generation by
		 operator overloading.

		 Unlike the 8051, ARM has many more registers, and each is 32 bits.
		 so for basic types, we can leave things in registers when evaluating
		 expressions, and the codecapsule should provide a method to tell
		 its user which register the value resides in.  once we can extract
		 the varAddress() of that result, we can use it to generate code.
		 this is true also with function calls, but we need to figure out
		 how GCC generates code.

		 The following comment is still leftover from 8051 and not yet updated for
		 ARM/thumb
		 - indicate where the latest result is stored
		 - specify where the result should go:
		 - query type of result
		 For type and representation
	'''
	_isa_constructor = ISAAVR
	_instr_size = 2  # each AVR instruction is 2 bytes (of unit size)

	def appendReturnValue(self):
		'''This method was moved from mapfile's grabReturnValue.
		   But strictly speaking, this is compiler dependent, not just ISA
			 dependent, right?

			20140207 NR: Return values: 8-bit in r24 (not r25!), 16-bit in
			r25:r24, up to 32 bits in r22-r25, up to 64 bits in r18-r25. 8-bit
			return values are zero/sign-extended to 16 bits by the called
			function (unsigned char is more efficient than signed char - just
			clr r25). Arguments to functions with variable argument lists
			(printf etc.) are all passed on stack, and char is extended to
			int.
			(http://www.nongnu.org/avr-libc/user-manual/FAQ.html#faq_reg_usage)
		'''
		t = self.getResultType()
		returnBufferAddress = self.getReturnBufferAddress()
		# Store return buffer address in Z
		self.emit('LDI ZL, 0x%x', returnBufferAddress & 0xFF)
		self.emit('LDI ZH, 0x%x', returnBufferAddress >> 8 & 0xFF)
		if (t == 'void') or (t is None):
			self.emit('LDI R%d, 0x%x', 25, 0)
			self.emit('ST Z+, R%d', 25)
		elif (sizeInBits(t) == 1):
			self.emit('CLR R%d', 24)
			self.emit('ROL R%d', 24)
			self.emit('ST Z+, R%d', 24)
		elif (sizeInBits(t) == 8):
			self.emit('ST Z+, R%d', 24)
		elif (sizeInBits(t) in (16, 32, 64)):
			x = sizeInBits(t)
			r = 25
			while x > 0:
				self.emit('ST Z+, R%d', r)
				r -= 1
				x -= 8
		else:
			raise TypeError('return type %s not supported' % t)

	def allocTemp(self, temp=None):
		return self._mcu.allocTemp(temp)

	def freeTemp(self, obj):
		self._mcu.freeTemp(obj)


	# def saveAinTemp(self, temp):
	# 	'''saves accumulator A into temp. This is hardwired...
	# 	 should generate code by assignment to handle different types
	# 	'''
	# 	self.emit('MOV R%d, A', temp.varAddress())

	# def allocTempBit(self, temp=None):
	# 	return self._mcu.allocTempBit(temp)

	# def freeTempBit(self, obj):
	# 	self._mcu.freeTempBit(obj)

	# def saveCinTempBit(self, temp):
	# 	self.emit('MOV 0x%x, C', temp.varAddress())

	def loadImm(self, imm, targetReg = 0):
		'''This generates the code to load an 8-bit immediate 
		   into the target register.
		'''
		self.emit('LDI R%d, 0x%x', targetReg, imm)

	def __add__(self, other):
		'''This overloads the + operator.  It assumes self and others have
		   been code-generated (or other can be an int).
			 ARM/Thumb handles 32-bit operations natively.
			 If 8-bit is added with 16-bit then should promote 8-bit first.
		'''
		if isinstance(other, int) or isinstance(other, str):
			# maybe code capsule needs to add type?
			# to model what kind it is.
			# check if int is 0. if so, skip it.
			if isinstance(other, str):
				if len(other) == 0:
					other = 0
				elif len(other) == 1:
					other = ord(other)
				else:
					raise ValueError('cannot yet add string')
			if (other != 0):
				# check range. Question: how to handle sign or unsigned? may need to
				# know on the host side when type-demarshaling?
				# should check self's type.
				t = self.getResultType()
				if sizeInBits(t) == 16:
					# do add followed by adc, but limited by immediate size.
					if (other <= 63) and (other >= 0):
						# we can use ADDIW, self's value assumed to be R25:24
						self.emit('ADIW R%d, 0x%x', 24, other)
					elif (other >= -255) and (other <= 0):
						# can use subtract immediate
						self.emit('SUBI R%d, 0x%x', 24, other) # lower byte, may borrow
						self.emit('SBCI R%d, 0x%x', 25, 0)
					else:  # load imm into temp register 
						checkRange(other, 16, isSigned(t))
						temp = self.allocTemp()
						self.loadImm(other & 0xff, temp.varAddress())
						self.emit('ADD R%d, R%d', 24, temp.varAddress())
						self.loadImm((other >> 8) & 0xff, temp.varAddress())
						self.emit('ADC R%d, R%d', 24, temp.varAddress())
						self.freeTemp(temp)
				elif sizeInBits(t) == 8:
					if (other <= 63) and (other >= 0):
						if isSigned(t): # sign-extend the upper byte R25
							# we can use ADDIW, but self is just R24. promote?
							self.emit('ADIW R25:24, 0x%x', other)
							self.emit('ROL R%d', 24) # put sign bit into C
							self.emit('CLR R%d', 25) # clear upper byte
							self.emit('SBC R%d', 25) # R25 = 0 - C, for sign extension
							# but do we set result type to int16?
						else:
							self.emit('CLR R%d', 25)
							self.emit('ADIW R25:24, 0x%x', other)
					elif (other >= -255) and (other <= 0):
						# can use subtract immediate
						self.emit('SUBI R%d, 0x%x', 24, other)
					else: # load immediate into temp and add
						checkRange(other, 8, isSigned(t))
						# this may be a bit restrictive: 8bit + 8bit only, no
						# promotion
						temp.self.allocTemp()
						self.loadImm(other, temp.varAddress())
						self.emit('ADD R%d, R%d', 24, other)
						self.freeTemp(temp)
					# should we call self.setResultType() to uint16 or int16 here?
					# or do it like 8051 and let self decide?
				else:  # sizeInBits(t) neither 8 nor 16 bit
					raise TypeError('type %s + int unsupported' % t)
			# else other = 0 => skip
		elif isinstance(other, CodeCapsule):
			t1 = self.getResultType()
			t2 = other.getResultType()
			if sizeInBits(t1) == 8 and sizeInBits(t2) == 8:
				# do the first, save result into temp, do second, and then add
				temp = self.allocTemp()
				# save self's result (R24) into a temp
				self.emit('MOV R%d, R%d', temp.varAddress(), 24)
				self.appendCode(other)
				self.emit('ADD R%d, R%d', 24, temp.varAddress())
				self.freeTemp(temp)
			elif sizeInBits(t1) == 16 and sizeInBits(t2) == 16:
				# push R25:24 onto stack
				self.emit('PUSH R%d', 25)
				self.emit('PUSH R%d', 24)
				self.appendCode(other)
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())
				self.emit('ADD R%d, R%d', 24, temp.varAddress())
				self.emit('POP R%d', temp.varAddress())
				self.emit('ADC R%d, R%d', 25, temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('unsupported type combination for add: %s + %s'\
						% (t1, t2))
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
				if len(other) == 0:  # i.e., treat empty string as zero
					other = 0
				elif len(other) == 1:
					other = ord(other)  # treat char (str of len 1) as ascii code
				else:
					raise ValueError('cannot subtract string')
			if (other != 0):
				# could also add the negated value
				t = self.getResultType()
				if sizeInBits(t) == 16: 
					checkRange(other, 16, isSigned(t))
					# self - 16bitInt
					if (other <= 63) and (other >= 0):
						# we can use subtract with immediate
						self.emit('SBIW R25:24, 0x%x', other)
					elif (other >= -63) and (other <= 0):
						# we can use adiw
						self.emit('ADIW R25:24, 0x%x', other)
					else:
						# load immediate and do as two subtracts
						self.emit('SUBI R%d, 0x%x', other & 0xff)
						self.emit('SBCI R%d, 0x%x', (other >> 8) & 0xff)
				elif sizeInBits(t) == 8:
					checkRange(other, 8, isSigned(t))
					self.emit('SUBI R%d, 0x%x', 24, other)
				else:
					raise TypeError('unsupported type %s in - operator' % t)
			# else, subtract 0, nothing to do
		elif isinstance(other, CodeCapsule):
			t1 = self.getResultType()
			t2 = other.getResultType()
			if sizeInBits(t1) == 8 and sizeInBits(t2) == 8:
				# we could use a register or a stack. here I'll do stack.
				self.emit('PUSH R%d', 24)  # save this value
				self.appendCode(other)         # put code for y
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())  # restore it back into 1
				self.emit('SUB R%d, R%d', 24, temp.varAddress()) # lower byte
			elif sizeInBits(t1) == 16 and sizeInBits(t2) == 16:
				self.emit('PUSH R%d', 25) # higher byte
				self.emit('PUSH R%d', 24) # lower byte
				self.appendCode(other)
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())
				self.emit('SUB R%d, R%d', 24, temp.varAddress())
				self.emit('POP R%d', temp.varAddress())
				self.emit('SBC R%d, R%d', 25, temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('mixed uint16 + uint8 not supported yet')
		else:
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __rsub__(self, other):
		'''
			sub is not commutative. simple way is to subtract and negate.
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
				if (other == 0): # can simply negate
					self.emit('NEG R%d', 24)
				else:
					checkRange(other, 8, isSigned(t))
					temp = self.allocTemp()
					self.emit('MOV R%d, R%d', temp.varAddress(), 24)
					self.emit('LDI R%d, 0x%x', 24, other)
					self.emit('SUB R%d, R%d', 24, temp.varAddress())
					self.freeTemp(temp)
			elif sizeInBits(t) == 16:
				chekRange(other, 16, isSigned(t))
				temp = self.allocTemp()
				self.emit('MOV R%d, R%d', temp.varAddress(), 24)
				self.emit('LDI R%d, 0x%x', 24, other & 0xff)
				self.emit('SUB R%d, R%d', 24, temp.varAddress())
				self.emit('MOV R%d, R%d', temp.varAddress(), 25)
				self.emit('LDI R%d, 0x%x', 25, (other >> 8) & 0xff)
				self.emit('SUBI R%d, R%d', 25, temp.varAdddress())
			else:
				raise TypeError('unsupported int - %s operation' % t)
		else: # not handled
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __and__(self, other):
		'''
			This is the bitwise AND operator.  Python does not allow the logical
			AND operator to be overridden.
		'''
		t = self.getResultType()
		# 
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 0 or other == False:
					self.emit('CLC') # clear C flag
				elif other == 1 or other == True:
					# essentially nop
					pass
				else:
					raise ValueError('bitwise-or type not bit: %s' % t)
			elif isinstance(other, CodeCapsule):
				t = other.getResultType()
				if sizeInBits(t) != 1:
					raise TypeError('bitwise-and type not bit' % t)
				temp = self.allocTemp()
				self.emit('CLR R%d', temp.varAddress())
				self.emit('ROL R%d', temp.varAddress()) # put C in temp reg
				self.appendCode(other)
				# now C has other's value
				self.appendCode('SBRS R%d, 0x%', temp.varAddress(), 0)
				# if saved bit is 1 then C is left unchanged
				# otherwise, force C flag to 0 whether it is already 0
				self.append('CLC') # set C = 0
				self.freeTemp(temp)
			else:
				raise ValueError('bitwise-and type unsupported: %s' % type(other))
		if sizeInBits(t) == 8:
			if isinstance(other, int):
				if (other == 0):  # AND'ing 0 => always 0
					# check if self's type is a bool, uint8, uint16, ...
					# we could simply make a new code capsule, right?
					self.emit('CLR R%d', 24)
				elif ((other & 0xff) != 0xFF):
					self.emit('ANDI R%d, 0x%x', 24, other)
				# otherwise it's a nop
			elif isinstance(other, CodeCapsule):
				# save self in temp, then do other, and AND
				temp = self.allocTemp()
				self.emit('MOV R%d, R%d', temp.varAddress(), 24) # save self in temp
				self.appendCode(other) # compute other
				self.emit('AND R%d, R%d', 24, temp.varAddress()) # compute AND
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types: %s and %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if other == 0:
				self.emit('CLR R%d', 24)
				self.emit('CLR R%d', 25)
			elif (other & 0xffff) != 0xffff:
				self.emit('ANDI R%d, 0x%x', 24, other & 0xff)
				self.emit('ANDI R%d, 0x%x', 25, (other >> 8) & 0xff)
			# otherwise nop
		elif isinstance(other, CodeCapsule):
			t2 = other.getResultType()
			if sizeInBits(t2) == 16: # save on stack
				self.emit('PUSH R%d', 25)
				self.emit('PUSH R%d', 24)
				self.appendCode(other)
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())
				self.emit('AND R%d, R%d', 24, temp.varAddress())
				self.emit('POP R%d', temp.varAddress())
				self.emit('AND R%d, R%d', 25, temp.varAddress())
				self.freeTemp(temp)
		else:
			raise TypeError('type %t not yet supported for and' % t)
		return self

	def __rand__(self, other):  # This is commutative
		return self.__and__(other)

	def __or__(self, other):
		t = self.getResultType()
		if sizeInBits(t) == 1:
			if isinstance(other, int) or isinstance(other, bool):
				if other == 1 or other == True:
					self.emit('SEC') # set carry flag
				elif other == 0 or other == False:
					# essentially nop
					pass
				else:
					raise ValueError('bitwise-or value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t = other.getResultType()
				if sizeInBits(t) != 1:
					raise ValueError('bitwise-or type not bit: %s' % t)
				temp = self.allocTemp()
				self.emit('CLR R%d', temp.varAddress())
				self.emit('ROL R%d', temp.varAddress()) # put C in temp reg
				self.appendCode(other)
				# now C has other's value
				self.appendCode('SBRC R%d, 0x%x', temp.varAddress(), 0)
				# if saved bit is 0 then C is left unchanged
				# otherwise, force C flag to 1 whether it is already 1
				self.appendCode('SEC') # set C = 1
				self.freeTemp(temp)
			else:
				raise ValueError('bitwise-and type unsupported: %s' % type(other))
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				if (other == 0xff):
					self.emit('LDI R%d, 0x%x', 24, 0xff)
				elif (other != 0):
					checkRange(other, 8, signed=False)
					self.emit('ORI R%d, 0x%x', 24, other)
				# else, OR'ing 0 is essentially a nop
			elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('bitwise-or type not byte: %s' % t2)
				temp = self.allocTemp()
				self.emit('MOV R%d, R%d', temp.varAddress(), 24) # save temp
				self.appendCode(other)
				self.emit('OR R%d, R%d', 24, temp.varAddress())
				self.freeTemp(temp)
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
					# xor with 0 => nop
					pass
				elif other == 1 or other == True:
					# essentially bit complement: could use sub to simulate it.
					# are there better ways to do it?
					temp = self.allocTemp()
					self.emit('CLR R%d', temp.varAddress())
					self.emit('SBCI R%d, 1', temp.varAddress()) # tmp = 1 - C
					self.emit('ROR R%d', templvarAddress()) # rotate low bit into C
					self.freeTemp(temp)
				else:
					raise ValueError('bitwise-xor value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('bitwise-xor type not bit: %s' % t2)
				temp = self.allocTemp()
				self.emit('CLR R%d', temp.varAddress())
				self.emit('ROL R%d', temp.varAddress()) # save C bit
				self.appendCode(other)
				# now do the same SBCI trick
				self.emit('SBCI R%d, 0', temp.varAddress()) # tmp = tmp - C
				self.emit('ROR R%d', temp.varAddress()) # put bit back into C
				self.freeTemp(temp)
			else:
				raise ValueError('bitwise-xor type not supported: %s' % other)
		elif sizeInBits(t) == 8:
			if isinstance(other, int):
				# check range?
				if other == 0xff:
					self.emit('COM R%d', 24)
				elif (other != 0): #nop
					temp = self.allocTemp()
					self.loadImm(other, temp.varAddress())  
					self.emit('EOR R%d, R%d', 24, temp.varAddress())
					self.freeTemp(temp)
				# otherwise essentially a nop
			elif isinstance(other, Capsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('bitwise-xor type not byte: %s' % t2)
				temp = self.allocTemp()
				self.emit('MOV R%d, R%d', temp.varAddress(), 24)
				self.appendCode(other)
				self.emit('EOR R%d, R%d', 24, temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('unsupported type for xor: %s' % type(other))
		elif sizeInBits(t) == 16:
			if isinstance(other, int):
				if (other == 0):
					pass
				elif other == 0xffff:
					# same as complement
					self.emit('COM R%d', 24)
					self.emit('COM R%d', 25)
				else:
					temp = self.allocTemp()
					self.emit('LDI R%d, 0x%x', temp.varAddress(), other & 0xff)
					self.emit('EOR R%d, R%d', 24, temp.varAddress())
					self.emit('LDI R%d, 0x%x', temp.varAddress(), (other>>8) & 0xff)
					self.emit('EOR R%d, R%d', 25, temp.varAddress())
					self.freeTemp(temp)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 16:
					raise TypeError('16-bit xor type not 16-bit: %s' % t2)
				self.emit('PUSH R%d', 25)
				self.emit('PUSH R%d', 24)
				self.appendCode(other)
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())
				self.emit('EOR R%d, R%d', 24, temp.varAddress())
				self.emit('POP R%d', temp.varAddress())
				self.emit('EOR R%d, R%d', 25, temp.varAddress())
				self.freeTemp(temp)
			else:
				raise TypeError('incompatible types: %s xor %s' % (t, type(other)))
		else: # includes 32-bit
			raise TypeError('unsupported type for xor' % type(other))
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
		'''this is the bit-invert operator. in ARM/THUMB, just NEG and -1'''
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# complement C
			temp = self.allocTemp()
			self.emit('CLR R%d', temp.varAddress()) # temp = 0
			self.emit('SBCI R%d, 0', temp.varAddress()) # temp = 1 - C
			self.emit('ROR R%d', temp.varAddress()) # C = temp<0>
			self.freeTemp(temp)
		elif sizeInBits(t) == 8:
			self.emit('COM R%d', 24)
		elif sizeInBits(t) == 16:
			self.emit('COM R%d', 24)
			self.emit('COM R%d', 25)
		else:
			raise TypeError('invert operator not supported for %s type' % t)
		return self

	def __neg__(self):
		'''this is the unary negation operator. we take two's complement.
		'''
		t = self.getResultType()
		if sizeInBits(t) == 1:
			# treat it as inverting a bit!
			return ~self
		if sizeInBits(t) == 8:
			self.emit('NEG R%d', 24)
		elif sizeInBits(t) == 16:
			self.emit('NEG R%d', 24) # 2's complement to lower
			self.emit('SBCI R%d, 0x%x', 25, 0) # trick: (upper - C)
			self.emit('COM R%d', 25) # ~(upper - C) = -(upper - C) - 1
							# = -upper + C - 1 = ~upper + 1 + C - 1 = ~upper + C
							# which is what we want!
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
					# nothing to do
					pass
				elif other == 0 or other == False:
					# complement C
					return ~self
				else:
					# well.. we could do a promotion of bit to int?
					raise ValueError('== value out of range: %s' % other)
			elif isinstance(other, CodeCapsule):
				t2 = other.getResultType()
				if sizeInBits(t2) != 1:
					raise TypeError('== type not bit: %s' % t2)
				temp = self.allocTemp()
				self.emit('CLR R%d', temp.varAddress())
				self.emit('ROL R%d', temp.varAddress()) # put C into temp
				self.appendCode(other)
				# for equality test, put them in int
				# assume we can trash R24
				self.emit('CLR R%d', 24)
				self.emit('ROL R%d', 24)
				# could use compare but let's do subtract, because we want to
				# leave the result in C as our bit accumulator.
				self.emit('SUB R%d, R%d', temp.varAddress(), 24) # if eq => 0
				self.emit('COM R%d', temp.varAddress()) # eq => 1
				self.emit('ROR R%d', temp.varAddress()) # C = eq bit
				self.freeTemp(temp)
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
				# compare here
				checkRange(other, 8, isSigned(t))
				temp = self.allocTemp()
				self.emit('LDI R%d, 0x%x', temp.varAddress(), 1)
				self.emit('CPI R%d, 0x%x', 24, other)
				self.emit('BREQ 0x%x', 1) # skip if equal
				self.emit('DEC R%d', 24) # if not equal, make it 0
				self.emit('ROR R%d', 24) # C = eq
			elif isinstance(other, CodeCapsule):
				# do the first, save result into temporary, do second, then
				# compare
				t2 = other.getResultType()
				if sizeInBits(t2) != 8:
					raise TypeError('%s == type not byte: %s' % (t, t2))
				temp = self.allocTemp()
				self.emit('MOV R%d, R%d', temp.varAddress(), 24)
				self.appendCode(other)
				self.emit('SUB R%d, R%d', 24, temp.varAddress())
				self.emit('COM R%d', 24) # not (not eq)
				self.emit('ROR R%d', 24) # C = eq
				self.freeTemp(temp)
			else:
				raise TypeError('incompatbile type for equality comparison: %s == %s' % (t, type(other)))
		elif sizeInBits(t) == 16:
			if (isistance(other, int)):
				# compare with int literal
				temp = self.allocTemp()
				self.emit('LDI R%d, 0x%x', temp.varAddress(), 1) # put 1 in temp
				# assume qual
				self.emit('CPI R%d, 0x%x', 24, other & 0xff)
				self.emit('BRNE 0x%x', 2) # jump to clear temp if not equal
				self.emit('CPI R%d, 0x%x', 25, (other >> 8) & 0xff)
				self.emit('BREQ 0x%x', 1) # skip clearing if equal
				self.emit('CLR R%d', temp.varAddress()) # clear if not equal
				self.freeTemp(temp)
			elif isinstance(other, CodeCapsule):
				# compare two 16-bit expressions
				self.emit('PUSH R%d', 25)
				self.emit('PUSH R%d', 24)
				self.appendCode(other)
				temp = self.allocTemp()
				self.emit('POP R%d', temp.varAddress())
				self.emit('SUB R%d, R%d', 24, temp.varAddress())
				self.emit('LDI R%d, 0x%x', temp.varAddress(), 1)
				self.emit('BRNE 0x%x', 2) # if SUB result == 0, continue compare
				self.emit('POP R%d', 24) # reuse R24 as temp!
				self.emit('CPSE R%d, R%d', 25, 24) # skip if upper bytes equal
				self.emit('CLR R%d', temp.varAddress()) # not equal => set to 0.
				self.emit('ROR R%d', temp.varAddress()) # in either case, put eq in C
				self.freeTemp(temp)
		else:
			raise TypeError('unsupported type for ==: %s' % t)
		self.setResultType('bool')
		return self

	def __ne__(self, other):
		return self._comp(other, 'BNE')

	def __lt__(self, other):
		return self._comp(other, 'BLT') # if LT, skip

	def __le__(self, other):
		return self._comp(other, 'BLE')

	def __ge__(self, other):
		return self._comp(other, 'BGE')

	def __gt__(self, other):
		return self._comp(other, 'BGT')

	def __mul__(self, other):
		'''This overloads the * operator for 32-bit operation.'''
		if isinstance(other, int):
			checkRange(other, 32, isSigned(t))
			if (other != 0):
				self.loadImm(other, 1) # R1 = other
				self.emit('MUL R%d, R%d', 0, 1)
		elif isinstance(other, CodeCapsule):
			self.emit('PUSH {R%d}', 0) # save R0
			self.appendCode(other)
			self.emit('POP {R%d}', 1) # restore into R1
			self.emit('MUL R%d, R%d', 0, 1)
		else:
			raise TypeError('Multiplying %s unsupported' % t)
		return self

	def __div__(self, other):
		'''Not yet implemented. see the document ARM7-TDMI-manual-pt3.pdf,
		Section 5.20.2 General purpose signed divide. 
		pasted here for convenience.
		signed_divide:
		; R1 / R0. returns quotient in R0, remainder in R1.
		; get abs
			ASR R2, R0, #31 ;  get 0 or -1 in R2 depending on sign of R0
			EOR R0, R2 ; EOR with -1 (0xFFFFFFFF) if negative
			SUB R3, R0, R2 ; and ADD 1 (SUB-1) to get absolute value
		; SUB always sets flag, so go and report div by 0 if necessary
		; BEQ divide_by_zero
		; Get abs value of R1 by xoring with 0xFFFFFFFF and adding 1
		; if negative
		  ASR R0, R1, #31  ; Get 0 or -1 in R3 depending on sign of R1
			EOR R1, R0       ; EOR with -1 if negative
			SUB R1, R0       ; and ADD 1 (sub 1) to get abs value
		; save signs (0 or -1 in R0 & R2) for later use in determining
		; sign of quotient and remainder
		  PUSH {R0, R2}
		; justification, shift 1 bit at a time until divisor (R0) 
		; is just <= dividend (R1 value). To do this shift dividend
		; right by 1 and stop as soon as shifted value becomes >.
		  LSR R0, R1, #1
			MOV R2, R3
			B  %FT0
		just_l  LSL R2, #1
		        CMP R2, R0
						BLS Just_l
						MOV R0, #0
						B  %FT0
		div_l   LSR R2, #1
		        CMP R1, R2   ; test subtract
						BCC %FT0
						SUB R1, R2
						ADC R0, R0
					  CMP R2, R3  ; terminate when R2==R3
						BNE div_l
						; now fix signs of quotient (R0) and remainder
						POP {R2, R3} ; get dividend/divisor signs back
						EOR R3, R2 ; result sign
						EOR R0, R3 ; negate if result sign = -1
						SUB R0, R3
						EOR R1, R2 ;  negate remainder if dividend sign = -1
						SUB R1, R2
						MOV PC, LR

				Divide by a constant. 
				see The ARM Cookbook (ARM DUYI-0005B) titled Division by a constant.
		'''
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
		if isinstance(other, int):
			# fixed number of positions
			# let's try it for each case.
			if other == 0:
				pass # nothing to do when you shift by 0
			elif (other < 0):
				# turn it into a right shift
				return self.__rshift__(self, -other)
			elif (other <= 31): # already includes (other >= 0)
				# do the left shift
				self.loadImm(other, 1)
				self.emit('LSL R%d, R%d, #0x%x', 0, 0, other)
			else: # just turn into all 0
				self.emit('MOV R%d, #0x%x', 0, 0)
		elif isinstance(other, CodeCapsule):
			self.emit('PUSH {R%d}', 0) # save this value
			self.appendCode(other)
			self.emit('POP {R%d}', 1) # restore this into R1
			self.emit('LSL R%d, R%d', 1, 0) # shift R1 by R0 positions
			self.emit('ADD R%d, R%d, #0x%x', 0, 1, 0) # mov result (R1) into R0
			# we need to use ADD #0 instead of MOV because MOV doesn't do R-R
			# map directly to the LSL instruction
		else:
			raise TypeError('left-shift not supported on %s' % self)
		return self

	def __rshift__(self, other):
		if isinstance(other, int):
			# fixed number of positions
			# let's try it for each case.
			if other == 0:
				pass # nothing to do when you shift by 0
			elif other < 0:
				# do it as left shift
				return self.__lshift(self, -other)
			elif (other <= 31): # already includes other >= 0
				self.loadImm(other, 1)
				# depending on if this is signed or unsigned
				if isSigned(self.getResultType()):
					# do arithmetic right shift
					self.emit('ASR R%d, R%d, #0x%x', 0, 0, other)
				else:
					self.emit('LSR R%d, R%d, #0x%x', 0, 0, other)
		elif isinstance(other, CodeCapsule):
			self.emit('PUSH {R%d}', 0) # save this result
			self.appendCode(other)
			self.emit('POP {R%d}', 1)  # restore this into R1
			if isSigned(self.getResultType()):
				self.emit('ASR R%d, R%d', 1, 0)
			else:
				self.emit('LSR R%d, R%d', 1, 0)
			self.emit('ADD R%d, R%d, #0x%x', 0, 1, 0)
		else:
			raise TypeError('right-shift not supported on %s' % self)
		return self

	def __getitem__(self, index):
		'''this is self[index]. This works on pointer type;
		   should we also have array type too?
			 To do: need a class for declaring a name as a pointer or array type.
		'''
		t = self.getResultType()
		if t[-1] == '*':
			elementType = t[:-1]
			sizeOfElement = sizeInBits(elementType)
			isElementSigned = isSigned(elementType)
			if sizeOfElement in [8, 16, 32]:
				# i.e., it's a pointer type, and the pointed unit size is a byte,
				# short, or word (1, 2, or 4 bytes).
				# compute the resulting address and load the unit
				if isinstance(index, int): # constant offset
					# we can use the appropriate instruction to load.
					# no need to multiply, because the instruction already scales.
					# combinations: 
					# load { byte, half, word } 
					# { sign extend, zero extend },
					# { imm offset, register offset }
					# imm offset is only 5 bits. so it is -16 to +15
					if isElementSigned or (index < -16) and (index > 15):
						# Thumb ISA requires sign-extended version to be R+R only.
						# we can use immediate mode
						self.loadImm(1, index << (sizeOfElement / 8))
						if sizeOfElement == 8:
							if isElementSigned: self.emit('LDSB R%d, [R%d, R%d]', 0, 0, 1)
							else:               self.emit('LDRB R%d, [R%d, R%d]', 0, 0, 1)
						elif sizeOfElement == 16:
							if isElementSigned: self.emit('LDSH R%d, [R%d, R%d]', 0, 0, 1)
							else:               self.emit('LDRH R%d, [R%d, R%d]', 0, 0, 1)
						else: # sizeOfElement == 32:
							# doesn't matter if it is signed or unsigned, just load
							self.emit('LDR R%d, [R%d, R%d]', 0, 0, 1)
					else: # element unsigned and range fittable by PC offset
						if (sizeOfElement == 8):    self.emit('LDRB R%d, [R%d, #%d]', 0, 0, index)
						elif (sizeOfElement == 16): self.emit('LDRH R%d, [R%d, #%d]', 0, 0, index << 1)
						else:                       self.emit('LDR R%d, [R%d, #%d]', 0, 0, index << 2)
									# 32 bits
					# all cases should be covered for constant index
				elif isinstance(index, CodeCapsule):
					t2 = index.getResultType()
					sizeOfIndexInBits = sizeInBits(t2)
					if sizeOfIndexInBits in [8, 16, 32]: # ok as index
						# save the base pointer
						self.emit('PUSH {R%d}', 0)
						self.appendCode(index)
						# shift left by 1 or 2 positions if not byte load
						if sizeOfIndexInBits == 16:
							self.emit('LSL R%d, R%d, #%d', 0, 0, 1)
						elif sizeOfIndexInBits == 32:
							self.emit('LSL R%d, R%d, #%d', 0, 0, 2)
						# restore base pointer, but in R1
						self.emit('POP {R%d}', 1)
						if sizeOfElement == 8: 
							if isElementSigned: self.emit('LDSB R%d, [R%d, R%d]', 0, 0, 1)
							else:               self.emit('LDRB R%d, [R%d, R%d]', 0, 0, 1)
						elif sizeOfELement == 16: 
							if isElementSigned: self.emit('LDSH R%d, [R%d, R%d]', 0, 0, 1)
							else:               self.emit('LDRH R%d, [R%d, R%d]', 0, 0, 1)
						else:                 self.emit('LDR R%d, [R%d, R%d]', 0, 0, 1)
					else:
						raise TypeError('array index of type %s unsupported' % t2)
				else: # it could be slice!  we should try to support this... maybe?
					raise TypeError('array index expression %s unsupported' % index)
			else:
				raise TypeError('array of type %s unsupported' % elementType)
			# if processed correctly, set the type of indexed expression
			# (uint8* becomes just uint8)
			self.setResultType(t[:-1])
		else:
			# not supported
			raise TypeError('Type %s cannot be indexed' % t)
		return self



	def __setitem__(self, index, value):
		'''this is self[index] = value.
		   we should evaluate RHS first;
			 then compute the index and then pointer for LHS,
			 and then do a store rather than a load.
			 should check if RHS and LHS have same type.
		'''
		if isinstance(value, int):
			# RHS into R0
			code = CodeCapsule(self._mcu, dest=self.getDest())
			code.loadImm(value)
		elif isinstance(value, CodeCapsule):
			code = value
		code.emit('PUSH {R%d}', 0)  # save value
		code.appendCode(self)  # now R0 has the base address
		tArray = self.getResultType()
		self.setCode(code)
		if tArray[-1] == '*' and sizeInBits(tArray[:-1]) in [8, 16, 32]:
			if isinstance(index, int):
				# might want to do a range check on the index, if length is known
				if isElementSigned or (index > 15) or (index < -16):
					# can only use R+R
					self.loadImm(index, 1)  # put index into R1
					self.emit('POP, {R%d}', 2) # restore value into R2
					if sizeOfElement == 8:
						self.emit('STRB R%d, [R%d, R%d]', 2, 0, 1)
					elif sizeOfElement == 16:
						self.emit('LSL R%d, R%d, #%d', 1, 1, 1) # index << 1
						self.emit('STRH R%d, [R%d, R%d]', 2, 0, 1)
					else:  # sizeOfElement == 32:
						self.emit('LSL R%d, R%d, #%d', 1, 1, 2) # index << 2
						self.emit('STR R%d, [R%d, #%d]', 2, 0, 1)
				else: # unsigned and small constant offset => can use immediate offset
					self.emit('POP {R%d}', 1) # restore value in R1. R0 is base addres.
					if sizeOfElement == 8:
						self.emit('STRB R%d, [R%d, #%d]', 1, 0, index)
					elif sizeOfElement == 16:
						self.emit('STRH R%d, [R%d, #%d]', 1, 0, index << 1)
					else: # sizeOfElement == 32:
						self.emit('STR R%d, [R%d, #%d]', 1, 0, index << 2)
			elif isinstance(index, CodeCapsule):
				self.emit('PUSH {R%d}', 0) # save base address
				self.appendCode(index) # now R0 has index
				self.emit('POP {R%d, R%d}', 1, 2) # R1 = base address, R2 = value
				if sizeOfElement == 8:
					self.emit('STRB R%d, [R%d, R%d]', 2, 1, 0)
				elif sizeOfElement == 16:
					self.emit('LSL R%d, R%d, #%d', 0, 0, 1)
					self.emit('STRH R%d, [R%d, R%d]', 2, 1, 0)
				else: # sizeOfElement == 32:
					self.emit('LSL R%d, R%d, #%d', 0, 0, 2)
					self.emit('STR R%d, [R%d, R%d]', 2, 1, 0)
			else:
				raise TypeError('unknown index type %s' % index)
			# cascaded assignment.
			self.setResultType(tArray[:-1])
			print self 
			# This is necessary because python interpreter ignores the
			# return value!  This is a hack for now. Eventually, we'll need to
			# invoke a function (from here and from __repr__()) to make the
			# network call, depending on interactive or code-gen mode.
			return self # this is a useless return self, but we do it anyway
		else:
			# other types of arrays not supported
			raise TypeError('array type %s unsupported' % tArray)


