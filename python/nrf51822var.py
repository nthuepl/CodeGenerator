'''
   This is an attempt to build up variables for nRF51822
	 I suppose a lot of it could be extracted out to a common ARM/THUMB,
	 but let's stick to nRF51822 for now.

	 Let's start with just simple ints. we'll add other types later.

	 Usage: the user creates a variable on the nRF51822 (MCU),
	 possibly by naming convention or by assignment?  or by
	 calling a "factory" to allocate or free a variable?
	 Actually, before full variables, we may also need temporary
	 variables, which may be mapped to stack or register access.

	 In 8051, variables need to have an associated storage class.
'''
import nrf51822sfr
from cc_thumb import CC_Thumb as CodeCapsule

class nRF51822VAR:
	'''
		this is the class for variables in nRF51822.
		declare its storage class, location, size, type, conversion,
		mapping (may need to be maintained by MCU!)
		we may allow overlays?
	'''
	_VAR = {
			'R0': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 0, },
			'R1': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 1, },
			'R2': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 2, },
			'R3': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 3, },
			'R4': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 4, },
			'R5': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 5, },
			'R6': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 6, },
			'R7': { 'storageClass': 'register', 'varType': 'int32',
						'varAddress': 7, },
			}

# some utility functions for type query

def sizeInBits(typeName):
	#if not VAR._typeDef.has_key(typeName):
	#	raise TypeError('unknown type %s' % typeName)
	# look up number of bits
	if typeName[-1] == '*':
		return 32
	else:
		return VAR._typeDef[typeName]['size']

def isSigned(typeName):
	return VAR._typeDef[typeName]['signed']



class VAR:
	_typeDef = {
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
	_storageClassDef = {
			'xdata': {
					'address':     32,
					'read':        8,       # access unit is 8, 16, 32 bit
					'write':       8,       # access unit is 8, 16, 32 bit
					'access':      'R/W',
					'pointable':   True,
					'overlayable': True, # thru flash mapping?
					'range': (0x20000000, 0x2003FFFF),
				},
			'code': {
					'address':     32,
					'read':        16,     # NOR flash can read 1 byte at a time
					'write':       16384, # 2KB page size as erase unit!
					'access':      'R',   # for all practical purpose
					'pointable':   True,
					'overlayable': True,  # thru SRAM mapping
					'range': (0x00000000, 0x00003FFF),
				},
			'register': {  # R0-R15
					'address':     4,  # 4 bits of pointer
					'read':        32,
					'write':       32,
					'access':      'R/W',
					'pointable':   False, # can't have a pointer to a register
					'overlayable': True,
				},

			'stackitem': {
					'address':     8,  # 8-bit offset from SP
					'read':        32,
					'write':       32,
					'access':      'R/W',
					'pointable':   True, # but dangerous...
					'overlayble':  True,
				},
		}


	def __init__(self, name, storageClass, varType, varAddress = None,
			mcu=None):
		'''constructor for nRF51822VAR.
		  storageClass is a string: 'char', 'int', 'long', 'bool',
			'uint8', 'unit16', 'unit32', etc. perhaps even a bit field
			or a slice can also be a var?  Actually, the same
			multi-word C types can all be used.

			extension to arrays, maybe also pointers.
			for now, allow arrays only for XDATA.
			format:
			- ('uint8', 20) -- to indicate 20-element array of uint8.
			  this can be extended to multiple dimensions, such as
				('uint8', 20, 30)
			- ('uint8', None) -- to indicate a size-unbounded array of uint8.
		'''
		if not self._storageClassDef.has_key(storageClass):
			raise TypeError('storage class %s not supported' % storageClass)
		if (isinstance(varType, tuple)):
			# look inside
			if not self._typeDef.has_key(varType[0]) or \
					not (sizeInBits(varType[0]) in [8, 16, 32]):
				raise TypeError('array %s of type %s not supported' % (name,
					varType[0]))
			# now check the dimensions
			if len(varType) != 2:
				raise TypeError('array %s - only 1-dimension is supported' % name)
			if not isinstance(varType[1], int):
				raise TypeError('array %s dimension must be int, got %s' % varType[1])
			if storageClass != 'xdata':
				raise TypeError('only xdata array is supported but got %s' % storageClass)
			# as a compound type, we use its element type?
			self._typeDefn     = self._typeDef[varType[0]]
		elif not self._typeDef.has_key(varType):
			raise TypeError('var %s of type %s not supported' % (name,varType))
		else:
			# this is one of the basic types.
			self._typeDefn     = self._typeDef[varType]
		# maybe should check address range?
		self._name         = name
		self._storageClass = storageClass
		self._storageDefn  = self._storageClassDef[storageClass]
		self._varType      = varType
		self._varAddress   = varAddress
		self._code         = None
		self._mcu          = mcu

	def getVarType(self):
		return self._varType

	def name(self):
		return self._name

	def varAddress(self):
		return self._varAddress

	def _checkRange(self, value):
		# should we stretch meaning of checkRange to mean index range of array!?
		# or, just raise exception
		if not isinstance(self._varType, str):
			raise TypeError('cannot check range for %s of %s type' % (self._name,
				self._varType))
		size = self._typeDefn['size']
		if (self._typeDefn['signed']):
			# valid range is -2**(size-1) to 2**(size-1)-1
			return -2**(size-1) <= value and value <= 2**(size-1)-1
		else:
			# valid range is 0 to 2**(size)-1
			return 0 <= value and value <= 2**(size) - 1

	def _loadImm(self, imm, targetReg):
		self._code.loadImm(imm, targetReg)

	def _readByte(self, storageClass, address):
		'''This method reads a byte from the var into register.
		   1/2/2014
			 the potential upgrade is to allow code capsule to yield
			 the register if it is already in a register.
			 To do: perhaps this function should be moved to CodeCapsule?
		'''
		if storageClass in ['xdata']:
			self._loadImm(address, 3) # by convention, use R3 for address
			# check if signed or unsigned
			if isSigned(self._varType):
				self._emit('LDSB R%d, [R%d, #%d]', 0, 3, 0) # R0 = R3[0]
			else:
				self._emit('LDRB R%d, [R%d, #%d]', 0, 3, 0) 
		elif storageClass in ['register']:
			# need register number... put into R0
			if address != 0:
				self._emit('MOV R%d, R%d', 0, address)
			# otherwise, already in R0
		elif storageClass in ['stackitem']:
			# do indirect stack addressing with offset
			# assume we can use R0 or R1 for indirect addressing
			if isSigned(self._varType):
				self._emit('LDSB R%d, [SP, #%d]', 0, address)
			else:
				self._emit('LDRB R%d, [SP, #%d]', 0, address)
		# elif self._storageClass in ['code' ]: - can't be code
		else:
			# not a supported storage class
			raise TypeError('attempt to load unsupported storage class %x'\
							% self._storageClass)

	def _readHalf(self, storageClass, address):
		'''This same as loadByte except load half
			 To do: perhaps this function should be moved to CodeCapsule?
		'''
		if storageClass in ['xdata']:
			self._loadImm(address, 3) # by convention, use R3 for address
			# check if signed or unsigned
			if isSigned(self._varType):
				self._emit('LDSH R%d, [R%d, #%d]', 0, 3, 0) # R0 = R3[0]
			else:
				self._emit('LDRH R%d, [R%d, #%d]', 0, 3, 0) 
		elif storageClass in ['register']:
			# need register number... put into R0
			if address != 0:
				self._emit('MOV R%d, R%d', 0, address)
			# otherwise, already in R0
		elif storageClass in ['stackitem']:
			# do indirect stack addressing with offset
			# assume we can use R0 or R1 for indirect addressing
			if isSigned(self._varType):
				self._emit('LDSH R%d, [SP, #%d]', 0, address)
			else:
				self._emit('LDRH R%d, [SP, #%d]', 0, address)
		# elif self._storageClass in ['code' ]: - can't be code
		else:
			# not a supported storage class
			raise TypeError('attempt to load unsupported storage class %x'\
							% self._storageClass)

	def _readWord(self, storageClass, address):
		'''This same as loadByte except load whole word
			 To do: perhaps this function should be moved to CodeCapsule?
		'''
		if storageClass in ['xdata']:
			self._loadImm(address, 3) # by convention, use R3 for address
			# check if signed or unsigned
			self._emit('LDR R%d, [R%d, #%d]', 0, 3, 0) 
		elif storageClass in ['register']:
			# need register number... put into R0
			if address != 0:
				self._emit('MOV R%d, R%d', 0, address)
			# otherwise, already in R0
		elif storageClass in ['stackitem']:
			# do indirect stack addressing with offset
			# assume we can use R0 or R1 for indirect addressing
			self._emit('LDR R%d, [SP, #%d]', 0, address)
		# elif self._storageClass in ['code' ]: - can't be code
		else:
			# not a supported storage class
			raise TypeError('attempt to load unsupported storage class %x'\
							% self._storageClass)

	def _emit(self, *instruction):
		self._code.emit(*instruction)

	def readVar(self, dest=None):
		'''This is to read from variable (by MOV, MOVX, SETB/CLR, ...).
		   if the var is an array, then do an LEA (load effective address),
			 and set the return type to be the type*.
			 e.g., for uint8[20], represented as ('uint8', 20),
			 the effective address has the type 'uint8*'.
		'''
		# assume we always have read permission for now. later restrict
		code = CodeCapsule(self._mcu, dest)
		self._code = code
		if isinstance(self._varType, tuple):
			# this is an array type.
			# like C, we just load its address without checking bounds for now,
			# though later we could try to check it.
			# again, assume only external memory for now.
			code.setResultType(self._varType[0]+'*')
			self._loadImm(self._varAddress, 0) # R0 = LEA(var)
			return code
		# others are regular scalar variables
		size = self._typeDefn['size'] # could be sizeInBits
		if size == 8:
			self._readByte(self._storageClass, self._varAddress)
		elif size == 16:
			self._readHalf(self._storageClass, self._varAddress)
		elif size == 32:
			self._readWord(self._storageClass, self._varAddress)
		else:
			raise Exception('reading variable of size %d not implemented' % size)
		if isSigned(self._varType):
			code.setResultType('int32')
		else:
			code.setResultType('uint32')
		return self._code

	def writeVar(self, value):
		'''This is to write the variable (by MOV, MOVX, SETB/CLR, ...) 
		   Option: check write permission?
			 Two ways to handle this: if RHS is another var (or SFR), then it
			 should be handled differently from a constant value.
		'''
		# allowed value: 
		# bool, int, str (1),

		# assigning a constant to a var. first check read-only
		if value is None:
			return
		if self._storageDefn['access'] == 'R':
			# uh oh, trying to write to read-only
			raise Exception('attempting to write to read-only memory')
		if isinstance(value, CodeCapsule):
			self._code = value
		else:
			# here we are assuming it is some literal expression
			self._code = CodeCapsule(self._mcu, dest=self)
			if (value == True):
				self._emit('MOV R%d, #0x%x', 0, 1)
				return self._code
			if (value == False):
				self._emit('MOV R%d, #0x%x', 0, 0)
				return self._code
			if (isinstance(value, int)):
				# if it is within range, i.e., 0..255, then use move
				if (value >= 0) and (value <= 255):
					self._emit('MOV R%d, #0x%x', value)
					return self._code
				if not self._checkRange(value):
					raise ValueError('%s is out of range for %s' % (value,
						self._storageClass))
				self._loadImm(value, 0)
				# Now the register R0 contains the value
				# depends on storage class
		if self._storageClass in ['xdata']:
			self._loadImm(self._address, 3) # use R3 for effective address
			size = sizeInBits(self._varType)
			if size == 8:
				self._emit('STRB R%d, [R%d, #%d]', 0, 3, 0)
			elif size == 16:
				self._emit('STRH R%d, [R%d, #%d]', 0, 3, 0)
			elif size == 32:
				self._emit('STR R%d, [R%d, #%d]', 0, 3, 0)
			else:
				raise TypeError('unsupported size %d of %s type' % (size,
					self._varType))
		elif self._storageClass in ['register']:
			pass # already in R0
		elif self._storageClass in ['stackitem']:
			size = sizeInBits(self._varType)
			if size == 8:
				self._emit('STRB R%d, [SP, #%d]', 0, self._address)
			elif size == 16:
				self._emit('STRH R%d, [SP, #%d]', 0, self._address)
			elif size == 32:
				self._emit('STR R%d, [SP, #%d]', 0, self._address)
			else:
				raise TypeError('unsupported size %d of %s type' % (size,
					self._varType))
		else:
				# not a supported storage class
				raise Exception('attempt to write to unsupported storage class %x'\
								% self._storageClass)
		# continue with code to write A to dest. conceptually
		# self._emit('MOV 0x%x, A', self._varAddress)
		return self._code

	def __repr__(self):
		return str(self.__class__.__name__+"('"+self._name+"')")

if __name__ == '__main__':
	g = globals()
	for varName in nRF51822VAR._VAR.keys():
		defn = nRF51822VAR._VAR[varName]
		storageClass = defn['storageClass']
		varType = defn['varType']
		varAddress = defn['varAddress']
		g[varName] = VAR(varName, storageClass, varType, varAddress)
	print nRF51822VAR._VAR.keys()
