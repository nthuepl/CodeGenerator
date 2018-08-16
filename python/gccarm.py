#
# gccarm.py
#
from cc_thumb import CC_Thumb as CodeCapsule
class MapFile:
	'''This is the mapfile data structure, which allows you to
		look up a function's info by name. 
		- type signature
		- code model:
		- addresses: 

		Note that this is just an example file that hardwires a lot of the
		data that is manually extracted from the map file.  In practice,
		these should be parsed from the map file and the source files
		(.c or .h), which can probably inferred from the file paths for
		the .r51 or .lib files (replace the suffix).
		---------
		This class is specific to each C source.
	'''

	_map = {}

class API:
	'''
		This class has a high chance of reuse over different ISAs.
		The parameter passing convention may be different though.
	'''
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


	# The following are no longer used for ARM/Thumb
	# def allocReg(self):
	# def popReg(self):
	# def allocRegPair(self):
	# def popRegPair(self):

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
		# passing according to GCC (actually ARM)'s passing convention.  See the doc
		# http://infocenter.arm.com/help/topic/com.arm.doc.ihi0042e/IHI0042E_aapcs.pdf
		# logical page 14
		# register r0 aka a1 = argument /result / scratch register 1.
		# register r1 aka a2 = argument / result / scratch register 2.
		# register r2 aka a3 = argument / scratch register 3.
		# register r3 aka a4 = argument / scratch register 4.
		# register r4 aka v1 = variable register 1
		# register r5 aka v2 = variable register 2
		# register r6 aka v3 = variable register 3
		# register r7 aka v4 = variable register 4
		# register r8 aka v5 = variable register 5
		# register r9: platform register; could be v6, SB, TR. probably I shouldn't use it.
		# register r10 aka v7 = variable register 7
		# register r11 aka v8 = variable register 8
		# register r12 aka IP = The Intra-Procedure-Call scratch register
		# register r13 = SP = stack pointer
		# register r14 = LR = link register
		# register r15 = PC = program counter.
		# the rest are supposed to be pushed on stack?
		# subroutine must preserve content of registers r4-r8, r10, r11, SP.
		# 
		# for values larger than 32 bits:
		# - double-word is passed in r0:r1 or r2:r3. content is in LDM instruction format
		# - 128-bit is passed in four consecutive registers.
		#
		# stack pointer must be word aligned.
		#
		# bit 0 of Link Register LR = 1 if BL called from Thumb, = 0 if ARM state.
		#
		# results: all promoted to word, returned in r0
		# double: r0:r1
		# quad: r0:r3
		#
		# order is strictly left to right.
		# registers are allocated on first-available, not most packed.
		self.regAvail  = [ 0, 1, 2, 3 ]  # registers available
		self.regStack = [ ]  # register numbers in order allocated
		self.regPairStack = [ ]  # tuples for register pairs allocated
		for (actual, formalType, formalName) in map(None, paramList, paramTypes, paramNames):
			# we check each parameter and (generate code to) push it on the
			# stack. Then we pop them to pass in the register(s).
			if isinstance(actual, int) or isinstance(actual, bool):
				# user passes an integer literal.
				# no need to generate code to evaluate them for now.
				# later, copy them directly to the registers involved.
				if sizeInBits(formalType) <= 32:
					# push takes a direct address. so need to put the imm in A,
					# and then push it as ACC.
					self.allocReg()
				elif sizeInBits(formalType) == 64:
					self.allocRegPair()
				else:
					raise TypeError('actual parameter type int mismatches with formal parameter type %s' % formalType )

			elif isinstance(actual, CodeCapsule):
				actualType = actual.getResultType()
				if sizeInBits(actualType) <= 32:
					if sizeInBits(formalType) <= 32:
						self.appendCode(actual)
						self.emit('PUSH ACC')  # for now, but should push _dest??
						self.allocReg()
					else:
						raise TypeError("passing %s to %s param unsupported" %\
								(actualType, formalType))
				elif sizeInBits(actualType) <= 64:
					# where do we put the two bytes?
					pass
				else:
					raise TypeError("passing %s as %s param unsupported" % \
									(actualType, formalType))
			else:
				raise ValueError("cannot pass %s as parameter" % type(actual))
		################# now pop the parameters to reg ##################
		F = paramTypes[-1::-1]
		A = paramList[-1::-1]
		for (formalType, actual) in map(None, F, A):
			# pop the parameter
			if sizeInBits(formalType) <= 32:
				regNum = self.popReg()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', regNum)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					# should probably check out of range
					self.emit('MOV R%d, #0x%x', regNum, actual)
				else:
					raise ValueError('%s not valid %s param' % (actual, formalType))
				# assume we use only register bank zero! 
				# this allows us to pop directly into the register's direct
				# address, because we can't pop into just a register.
			elif sizeInBits(formalType) <= 64:
				# similar to int except we need to do two bytes.
				higher, lower = self.popRegPair()
				if isinstance(actual, CodeCapsule):
					self.emit('POP 0x%x', higher)
					self.emit('POP 0x%x', lower)
				elif isinstance(actual, int) or isinstance(actual, bool):
					actual = int(actual)
					self.emit('MOV R%d, #0x%x', higher, (actual >> 8) & 0xff)
					self.emit('MOV R%d, #0x%x', lower, actual & 0xff)
				else:
					raise ValueError('%s not valid %s param' % (actual, formalType))
			else:
				raise TypeError("param type %s not supported" % formalType)

	def makeCall(self):
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
		<= 32-bit value: R0
		64-bit value: R1:R0
		quadword value: R3:R0
    Our format:
		[length][byte 0][byte 1][byte 2][byte 3]
		'''
		t = self._info['returnType']
		self._code.setResultType(t)
