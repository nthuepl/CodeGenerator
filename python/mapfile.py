#
# mapfile.py
#
from codecapsule import CodeCapsule
from cc_8051 import sizeInBits, isSigned

class MapFile:
	'''This is the mapfile data structure, which allows you to
		look up a function's info by name. 
		- type signature
		- code model:
		  - near (16-bit pointer),
			- far (24-bit pointer),
			- banked code with relay
		- addresses: 
		  - function's address
			- ?CALL_IND's address (library function for making near or far
				calls, or making banked indirect function call.)
			- ?BDISPATCH's address (library function for making banked call)
			- ??function?relay address (auto generated for each function)

		Note that this is just an example file that hardwires a lot of the
		data that is manually extracted from the map file.  In practice,
		these should be parsed from the map file and the source files
		(.c or .h), which can probably inferred from the file paths for
		the .r51 or .lib files (replace the suffix).
	'''
	import dic_manual
	_map = dic_manual._map
	# the automatically generated one is dic_auto.py


class API:
	def __init__(self, name, mcu):
		if not mcu._mapAPI.has_key(name):
			raise NameError("name %s not in map file" % name)
		self._name = name
		# look up the info
		self._info = mcu._mapAPI[name]
		self._mcu = mcu

	def appendCode(self, cap):
		'''a pass-through for code capsule operaton'''
		self._code.appendCode(cap)

	def emit(self, formatStr, *operands):
		self._code.emit(formatStr, *operands)

	def __call__(self, *param):
		'''this object is being *called* with the parameter.
				we need to check and typecast the parameters.
				Two phases:
				(1) we code-gen each item and pass as parameter, by
						allocating the designated parameter registers.
				(2) generate code to make the call, to the relay function if
						necessary.
				(3) generate code to fetch the return value, and
						free up the parameter registers.
		'''
		# generate code for passing parameters
		self.passParam(*param)
		# generate code for making the call
		self.makeCall()
		# generate code for fetching the return value
		self.grabReturnValue()
		return self._code

	def allocUint8Reg(self):
		'''This is a private method for allocating a register for uint8
			parameter
		'''
		if len(self.regAvail) == 0:
			raise ValueError('param register overflow - stack not implemented')
		regNum = self.regAvail.pop(0)
		self.uint8Stack.append(regNum)

	def popUint8Reg(self):
		return self.uint8Stack.pop()

	def allocBitReg(self):
		'''This is a private method for allocating a register for a
			boolean (bit) parameter
		'''
		if (len(self.boolStack) >= 8):
			raise ValueError('bit params overflow - VB not implemented')
		self.boolStack.append(len(self.boolStack))

	def popBitReg(self):
		'''This is a private method that does the reverse of allocBitReg
		   by popping it off the stack and return its number
		'''
		return self.boolStack.pop()

	def allocUint16Reg(self):
		if (3 in self.regAvail) and (2 in self.regAvail):
			# allocate them for param passing
			self.uint16Stack.append((2,3))
			self.regAvail.remove(2)
			self.regAvail.remove(3)
		elif (5 in self.regAvail) and (4 in self.regAvail):
			self.uint16Stack.append((4,5))
			self.regAvail.remove(4)
			self.regAvail.remove(5)
		else:
			raise ValueError('out of registers for passing uint16 param')

	def popUint16Reg(self):
		return self.uint16Stack.pop()
		# no need to replenish regAvail, because that is always
		# replenished by the next passParam

	def passParam(self, *paramList):
		'''this is the helper method to generate code to pass parameters
			to a function call. the paramList is essentially a list of
			code capsules. one issue is with the use of registers and
			accumulators. we could try to lock down parameter registers
			(but we would have no way to know at the time of code gen)
			but the surest way is to 
			- code-gen each param expression and push each onto stack before
				code-gen and push next, including bits too!
			- after pushing everything on stack, copy (and pop) each 
			  into the register(s). 
			The use of stack is what enables arbitrary expressions,
			including function call expressions, as parameter values.
			e.g., f(g(x+h(y))-i)
		'''
		paramTypes = self._info['paramTypes']
		paramNames = self._info['paramNames']
		if (len(paramTypes) != len(paramNames)):
			raise AttributeError('param type list and param name list mismatch')
		# now make sure we have the right number of actual parameters 
		# we don't (yet) support variable parameter list or passing by
		# name, but eventually we probably can.
		if len(paramList) != len(paramTypes):
			raise TypeError('parameter list mismatch: %d expected, %d passed' %\
					(len(paramTypes), len(paramList)))
		# check and convert type if necessary
		self._code = CodeCapsule(self._mcu)
		################# evaluate each parameter ##################
		# Now define some variables for register allocation for param
		# passing according to IAR's passing convention.  See the doc
		# EW8051_compilerreference.pdf phyisical page 167, logical page 135
		# 1-bit values: B.0,...B.7, VB.0, ..VB.7
		# 8-bit values: R1, ...R5
		# 16-bit values: R3:R2 or R5:R4.
		# 32-bit values: R5:R2
		# the rest are supposed to be pushed on stack.
		# order is strictly left to right.
		# registers are allocated on first-available, not most packed.
		self.boolStack = [ ]  # stack of boolean variables
		self.regAvail  = [ 1, 2, 3, 4, 5 ]  # registers available
		self.uint8Stack = [ ]  # register numbers in order allocated
		self.uint16Stack = [ ]  # tuples for register pairs allocated
		for (actual, formalType, formalName) in map(None, paramList, paramTypes, paramNames):
			# we check each parameter and (generate code to) push it on the
			# stack. Then we pop them to pass in the register(s).
			if isinstance(actual, int) or isinstance(actual, bool):
				# user passes an integer literal.
				# no need to generate code to evaluate them for now.
				# later, copy them directly to the registers involved.
				sizeOfFormalInBits = sizeInBits(formalType)
				if sizeOfFormalInBits == 8:
					# push takes a direct address. so need to put the imm in A,
					# and then push it as ACC.
					# self.emit('MOV A, #0x%x', actual)
					# self.emit('PUSH ACC')
					self.allocUint8Reg()
				elif sizeOfFormalInBits == 1:
					# the only thing is maybe check overflow
					if (actual < 0) or (actual > 1):
						raise ValueError('actual parameter %s overflows for boolean' \
								% actual)
					# self.emit('MOV A, #0x%x', actual)  # load literal value
					# self.emit('PUSH ACC')  # push value onto stack
					self.allocBitReg()

				elif sizeOfFormalInBits == 16 or formalType[-1] == '*':
					# we treat (data) pointer as uint16.
					# Need to check if callback pointers can still work by passing the
					# address of the 16-bit relay.
					# push two bytes, little-endian byte order
					# use DPTR - saves one byte and a few cycles
					# self.emit('MOV DPTR, #0x%x', actual)
					# self.emit('PUSH DPL0') # we assume DPTR0
					# self.emit('PUSH DPH0') # we assume DPTR0
					# try R3:R2, then R5:R4
					self.allocUint16Reg()
				else:
					raise TypeError('actual parameter type int mismatches with formal parameter type %s' % formalType )

			elif isinstance(actual, CodeCapsule):
				actualType = actual.getResultType()
				if actualType == 'bool':
					# if bit, push entire Carry. somewhat wasteful but it's a
					# price to pay
					if formalType == 'bool':
						self.appendCode(actual)
						self.emit('PUSH PSW')
						self.allocBitReg()
					elif formalType == 'uint8':
						# should convert boolean to a byte. Clear A and rotate C in.
						self.appendCode(actual) # assume actual's code puts it into C
						self.emit('CLR A')  # set A = 0
						self.emit('RLC')    # rotate C into A.0
						self.emit('PUSH ACC')
						self.allocUint8Reg()
					else:
						raise TypeError("passing %s to %s param unsupported" %\
								(actualType, formalType))
				elif actualType == 'uint8':
					if formalType == 'uint8':
						self.appendCode(actual)
						self.emit('PUSH ACC')  # for now, but should push _dest??
						self.allocUint8Reg()
					else:
						# if formalType == 'bool':
							# we could convert this to boolean? based on zero or
							# nonzero? but for now we don't allow it. can always do
							# != 0 to force conversion.
						raise TypeError("passing %s to %s param unsupported" %\
								(actualType, formalType))
				elif actualType == 'uint16' or actualType[-1] == '*':
					# where do we put the two bytes?
					pass
				else:
					raise TypeError("passing %s as %s param unsupported" % \
									(actualType, formalType))
			else:
				raise ValueError("cannot pass %s as parameter" % type(actual))
		################# now pop the parameters to reg ##################
		# We don't do this step in SDCC.  Instead, we go with the 
		# simpler way -- we push things onto the internal stack as we go!
		# we will need to pop them upon return, right?
		##################################################################
		F = paramTypes[-1::-1]
		A = paramList[-1::-1]
		for (formalType, actual) in map(None, F, A):
			# pop the parameter
			if formalType == 'bool':
				regNum = self.popBitReg()
				if isinstance(actual, CodeCapsule):
					# pop back to ACC, rotate into CY, then 
					self.emit('POP ACC') # pop whole PSW back into A
					self.emit('RRC')     # rotate right to get A.0 into C 
					self.emit('MOV B.%d, C', self.popBitReg())
				elif isinstance(actual, bool) and (actual == True) or \
						isinstance(actual, int) and (actual == 1):
					# literal value 1 or True
					self.emit('SETB B.%d', regNum)
				elif isinstance(actual, bool) and (actual == False) or \
						isinstance(actual, int) and (actual == 0):
					# literal value 0 or False
					self.emit('CLR B.%d', regNum)
				else:
					# probably out of range?
					raise ValueError('%s not valid boolean param' % actual)
			elif formalType == 'uint8':
				regNum = self.popUint8Reg()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', regNum)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					# should probably check out of range
					self.emit('MOV R%d, #0x%x', regNum, actual)
				else:
					raise ValueError('%s not valid uint8 param' % actual)
				# assume we use only register bank zero! 
				# this allows us to pop directly into the register's direct
				# address, because we can't pop into just a register.
			elif formalType == 'uint16' or formalType[-1] == '*':
				# similar to unit8 except we need to do two bytes.
				higher, lower = self.popUint16Reg()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', higher)
					self.emit('POP 0x%x', lower)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					self.emit('MOV R%d, #0x%x', higher, (actual >> 8) & 0xff)
					self.emit('MOV R%d, #0x%x', lower, actual & 0xff)
				else:
					raise ValueError('%s not valid uint16 param' % actual)
			else:
				raise TypeError("param type %s not supported" % formalType)

	def makeCall(self):
		'''make either a direct call or call the relay function'''
		if self._info.has_key('relay'):
			# make a call to relay function
			self.emit('LCALL 0x%x', self._info['relay'])
		else:
			# make a direct call to its address
			self.emit('LCALL 0x%x', self._info['address'])


	def grabReturnValue(self):
		'''
		12/20/2013: This method should be changed in the following ways:
		- it should set the return type in CodeCapsule but not generate
		  the code to grab return value -- CodeCapsule should do that.
		- this method should, however, move 8-bit return value from R1 to A.
		  this is assumed by everyone else.
		- It would be nice to have a code optimization pass so we can eliminate
		  unnecessary copying, but this would require knowing basic blocks.

		this method generates the code that immediately follows the
		LCALL instruction. it should grab the return value and put it
		into the return buffer.
		See Table 31, page 137 of the EW8051_compilerreference document.
		we assume little endian here , which is not external stack.
		1-bit value: C
		8-bit value: R1
		16-bit value: R3:R2
		24-bit value: R3:R2:R1
		32-bit value: R5:R4:R3:R2
    Our format:
		[length][byte 0][byte 1][byte 2][byte 3]
		'''
		t = self._info['returnType']
		self._code.setResultType(t)
		if (t == 'uint8'):
			self.emit('MOV A, R1')
