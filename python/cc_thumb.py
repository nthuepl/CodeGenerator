# cc_thumb.py
# this is code capsule for thumb instruction set
# it was thumb.py but renamed with cc_ file prefix to indicate
# the restructuring to be a subclass of CodeCapsule.
#
from codecapsule import CodeCapsule
from isa_thumb import ISAThumb
import nrf51822var

def sizeInBits(typeName):
	return nrf51822var.sizeInBits(typeName)

def isSigned(typeName):
	return nrf51822var.isSigned(typeName)

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


class CC_Thumb(CodeCapsule):
	'''This is the code capsule class for the THUMB ISA.
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
	_isa_constructor = ISAThumb
	_instr_size = 2  # each thumb instruction is 2 bytes

	def appendReturnValue(self):
		'''This method was moved from mapfile's grabReturnValue.
		   But strictly speaking, this is compiler dependent, not just ISA
			 dependent, right?
		'''
		t = self.getResultType()
		self.loadImm(self.getReturnBufferAddress(), 3) # R3 = buf address
		if (t == 'void') or (t is None):
			# just set length = 0
			self.emit('MOV R%d, #0x%x', 0, 0) # R0 = 0
		elif (sizeInBits(t) <= 32):
			# store the length = 4 bytes
			self.emit('MOV R%d, #0x%x', 0, 4) # R0 = 4
		else:
			raise TypeError('return type %s not supported' % t)
		self.emit('STR R%d, [R%d, #%d]', 0, 3, 0) # R3[0] = R0


	# def allocTemp(self, temp=None):
	# 	return self._mcu.allocTemp(temp)

	# def freeTemp(self, obj):
	# 	self._mcu.freeTemp(obj)


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
		'''This generates the code to load an immediate using PC relative mode
		   into the target register.  target is assumed to be R0 by default.
			 Assume the code starts with word boundary.
		'''
		# strategy: load effective address as 32-bit data from PC-relative location
		# and use unconditional Branch to skip the 32-bit address.
		self.emit('LDR R%d, [PC, #%d]', targetReg, 0) # from (PC+4) + 0
		self.emit('B 0x%x', 0) # target PC is offset from PC + 4
		self.emit('.word 0x%x', imm) # this is the actual "immediate"

	def __add__(self, other):
		'''This overloads the + operator.  It assumes self and others have
		   been code-generated (or other can be an int).
			 ARM/Thumb handles 32-bit operations natively.
			 If 8-bit is added with 16-bit then should promote 8-bit first.
		'''
		if isinstance(other, int):
			# maybe code capsule needs to add type?
			# to model what kind it is.
			# if it is in A, then just add A!!
			# check if int is 0. if so, skip it.
			if (other != 0):
				# check range. Question: how to handle sign or unsigned? may need to
				# know on the host side when type-demarshaling?
				# should check self's type.
				if (other <= 255) and (other >= 0):
					# we can use the brief version of ADD
					self.emit('ADD R%d, #0x%x', 0, other)
				elif (other >= -255) and (other < 0):
					# use subtract
					self.emit('SUB R%d, #0x%x', 0, -other)
				else:
					checkRange(other, 32, isSigned(t)) 
					self.loadImm(other, 1) # R1 = other
					self.emit('ADD R%d, R%d', 0, 1)
			# else other = 0 => skip
		elif isinstance(other, CodeCapsule):
			# first, check if both 32-bit
			self.emit('PUSH {R%d}', 0) # save this value
			self.appendCode(other)  # add code from other
			self.emit('POP {R%d}', 1) # restore but back into R1
			self.emit('ADD R%d, R%d', 0, 1) # add the two, leave in R0 (~accumulator)
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
		if isinstance(other, int):
			if (other != 0):
				# could also add the negated value
				if (other <= 255) and (other >= 0):
					# we can use subtract
					self.emit('SUB R%d, #0x%x', 0, other)
				elif (other >= -255) and (other < 0):
					# we can use add
					self.emit('ADD R%d, #0x%x', 0, other)
				else:
					checkRange(other, 32, isSigned(t))
					self.loadImm(other, 1) # R1 = other
					self.emit('SUB R%d, R%d', 0, 1)
			# else, subtract 0, nothing to do
		elif isinstance(other, CodeCapsule):
			self.emit('PUSH {R%d}', 0)  # save this value
			self.appendCode(other)         # put code for y
			self.emit('POP {R%d}', 1)  # restore it back into 1
			self.emit('SUB R%d, R%d, R%d', 0, 1, 0) # R0 = R1 - R0
		else:
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __rsub__(self, other):
		'''
			sub is not commutative. simple way is to subtract and negate.
		'''
		if isinstance(other, int):
			if (other == 0):
				# we simply negate
				self.emit('NEG R%d, R%d', 0, 0)
			elif (other <= 255) and (other >= 0):
				# we can subtract and negate
				self.emit('SUB R%d, #0x%x', 0, other)
				self.emit('NEG R%d, R%d', 0, 0)
			elif (other >= -255) and (other < 0):
				# we first add and then negate the result
				self.emit('ADD R%d, #0x%x', 0, other)
				self.emit('NEG R%d, R%d', 0, 0)
			else:
				checkRange(other, 32, isSigned(t))
				self.loadImm(other, 1) # R1 = other
				self.emit('SUB R%d, R%d, R%d', 0, 1, 0)
		elif isinstance(other, CodeCapsule):
			self.emit('PUSH {R%d}', 0) # save this value
			self.appendCode(other)  # push code for x
			self.emit('POP {R%d}', 1)  # restore back
			self.emit('SUB R%d, R%d, R%d', 0, 0, 1) # R0 = x - y
		else: # not handled
			raise TypeError('type not supported for -: %s' % type(other))
		return self

	def __and__(self, other):
		'''
			This is the bitwise AND operator.  Python does not allow the logical
			AND operator to be overridden.
		'''
		if isinstance(other, int):
			if (other == 0):  # AND'ing 0 => always 0
				# check if self's type is a bool, uint8, uint16, ...
				# we could simply make a new code capsule, right?
				self.emit('MOV R%d, #0x%x', 0, 0)
			elif (other != 0xFFFFFFFF) and (other != -1):
				checkRange(other, 32, signed=False)
				# should we check range?  should we limit it to 32 bits?
				self.loadImm(other, 1) # put immediate into R1
				self.emit('AND R%d, R%d', 0, 1)
			# else nothing to do
		elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
				# may need to check array or struct
				self.emit('PUSH {R%d}', 0) # save this register
				self.appendCode(other)  # take code already generated,
				self.emit('POP {R%d}', 1)
				self.emit('AND R%d, R%d', 0, 1)
		else:
			raise TypeError('unsupported type for and: %s' % t)
		return self

	def __rand__(self, other):  # This is commutative
		return self.__and__(other)

	def __or__(self, other):
		if isinstance(other, int):
			# should we check range?
			if (other == 0xffffffff) or (other == -1): # OR'ing ff => always ff
				self.emit('MOV R%d, #0x%x', 0xffffffff)
			elif (other != 0):
				checkRange(other, 32, signed=False)
				self.loadImm(other, 1)
				self.emit('ORR R%d, R%d', 0, 1)
			# else, essentially a nop
		elif isinstance(other, codecapsule.CodeCapsule):
			# do the first, save the result into a temporary, do the second,
			# and then add.
			self.emit('PUSH {R%d}', 0)  # save this register
			self.appendCode(other)  # take code already generated,
			self.emit('POP {R%d}', 1)  # restore this but in R1
			self.emit('ORR R%d, R%d', 0, 1)
		else:
			raise TypeError('unsupported type for or: %s' % t)
		return self

	def __ror__(self, other):
		return self.__or__(other)

	def __xor__(self, other):
		if isinstance(other, int):
			# check range?
			if (other != 0): #nop
				self.loadImm(other, 1)  # put immediate into R1
				self.emit('EOR R%d, R%d', 0, 1)
		elif isinstance(other, Capsule):
			self.emit('PUSH {R%d}', 0)  # save R0
			self.appendCode(other)  # take code already generated,
			self.emit('POP {R%d}', 1)   # restore self value but in R1
			self.emit('EOR R%d, R%d', 0, 1)
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
		'''this is the bit-invert operator. in ARM/THUMB, just NEG and -1'''
		self.emit('NEG R%d', 0)
		self.emit('SUB R%d, #0x%x', 0, 1)
		return self

	def __neg__(self):
		'''this is the unary negation operator. we take two's complement.
		'''
		self.emit('NEG R%d', 0)
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

	def _comp(self, other, opcode):
		'''This is common routine shared by all six comparison operators.'''
		if isinstance(other, int):
			# if within range, we can use the imm in CMP
			if (other >= 0) and (other <= 255): 
				# use immediate
				self.emit('CMP R%0, #0x%x', 0, other)
			else:
				# need to load immediate 
				self.loadImm(other, 1) # R1 = other
				self.emit('CMP R%d, R%d', 0, 1)
			# in either case, we can put comparison result into R0
			self.emit('MOV R%d, #0x%x', 0, 1) # by default, set to true
			self.emit(opcode + ' 0x%x', 0)  # if equal, skip
			self.emit('MOV R%d, #0x%x', 0, 0) # [PC+4]-2 else, set to false
			# here is [PC+4]+0
		elif isinstance(other, CodeCapsule):
				# do the first, save the result into a temporary, do the second,
				# and then add.
			self.emit('PUSH {R%d}', 0) # save R0
			self.appendCode(other)  # take code already generated,
			self.emit('POP {R%d}', 1) # restore self but into R1
			self.emit('CMP R%d, R%d', 1, 0) 
			self.emit('MOV R%d, #0x%x', 0, 1) # by default, set to true
			self.emit(opcode + ' 0x%x', 0)  # if equal, skip
			self.emit('MOV R%d, #0x%x', 0, 0) # [PC+4]-2 else, set to false
		else:
			# other types can be implemented later, but may
			# require converting to longer types.
			raise TypeError('unsupported type for comparison: %s' % t)
		return self

	def __eq__(self, other):
		return self._comp(other, 'BEQ')

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


