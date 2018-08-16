'''
   This is an attempt to build up variables for nRF24E1.
	 It is copied from cc2540var.py as a starting point.

	 Usage: the user creates a variable on the nRF24E1MCU,
	 possibly by naming convention or by assignment?  or by
	 calling a "factory" to allocate or free a variable?
	 Actually, before full variables, we may also need temporary
	 variables, which may be mapped to stack or register access.

	 In 8051, variables need to have an associated storage class.
'''
import nrf24e1sfr
from cc_8051 import CC_8051 as CodeCapsule

class nRF24E1VAR:
	'''
		this is the class for variables in CC2540.
		declare its storage class, location, size, type, conversion,
		mapping (may need to be maintained by MCU!)
		we may allow overlays?
	'''
	_VAR = {
			'A':  { 'storageClass': 'accumulator', 'varType': 'uint8',
							'varAddress':  None, },
			'C':  { 'storageClass': 'carrybit', 'varType': 'bool',
							'varAddress': None, },
			'R0': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 0, },
			'R1': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 1, },
			'R2': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 2, },
			'R3': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 3, },
			'R4': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 4, },
			'R5': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 5, },
			'R6': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 6, },
			'R7': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 7, },

			'DPTR': { 'storageClass': 'SFR16', 'varType': 'uint16',
						'varAddress': [0x82, 0x83], }, # DPL, DPH
			'ADC_DATA': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0xA3, 0xA2], }, # ADC_DATAL, ADC_DATAH @@@ need to check these addresses?
			'RCAP2': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0xCA, 0xCB], }, # RCAP2 (timer/counter 2 capture or reload)
			'T0': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0x8A, 0x8C], }, # Timer 2 low and high bytes
			'T1': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0x8B, 0x8D], }, # Timer 2 low and high bytes
			'T2': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0xCC, 0xCD], }, # Timer 2 low and high bytes
			 #### We don't support VB register -- what is it!? ####
			 'R3R2': { 'storageClass': 'register', 'varType': 'uint16',
				 'varAddress': [0x3, 0x2] },
			 'R5R4': { 'storageClass': 'register', 'varType': 'uint16',
				 'varAddress': [0x5, 0x4] },
			 'R3R2R1': { 'storageClass': 'register', 'varType': 'uint24',
				 'varAddress': [0x3, 0x2, 0x1] },
			 'R5R4R3R2': { 'storageClass': 'register', 'varType': 'uint32',
				 'varAddress': [0x5, 0x4, 0x3, 0x2] },
			 'tempBit0': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x08 },
			 'tempBit1': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x09 },
			 'tempBit2': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0a },
			 'tempBit3': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0b },
			 'tempBit4': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0c },
			 'tempBit5': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0d },
			 'tempBit6': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0e },
			 'tempBit7': { 'storageClass': 'bitMem', 'varType': 'bool',
					 'varAddress': 0x0f },
			}

# some utility functions for type query

def sizeInBits(typeName):
	#if not VAR._typeDef.has_key(typeName):
	#	raise TypeError('unknown type %s' % typeName)
	# look up number of bits
	if typeName[-1] == '*':
		return 16
	else:
		return VAR._typeDef[typeName]['size']

def isSigned(typeName):
	return VAR._typeDef[typeName]['signed']



class VAR:
	_typeDef = {
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
	_storageClassDef = {
			'bitMem': { # bit addressable memory area
					'address':   8,       # using 8-bit address
					'read':      1,       # access unit is 1 bit
					'write':     1,
					'access':    'R/W',    # by default, 
					'pointable':  False, # can't reference thru pointer
					'overlayable': True, # but could still be modified thru overlay
				},
			'iram': {   # internal, lower 128 byte minus the registers
					'address':     8,
					'read':        8,       # access unit is 8 bit
					'write':       8,       # access unit is 8 bit
					'access':      'R/W',
					'pointable':   True,
					'overlayable': True,
				},
			'uram': {   # upper 128-byte internal RAM, indirect addressing only
					'address':     8,
					'read':        8,
					'write':       8,
					'access':      'R/W',
					'pointable':   True,
					'overlayable': True,
				},
			'xdata': {
					'address':     16,
					'read':        8,       # access unit is 8 bit
					'write':       8,       # access unit is 8 bit
					'access':      'R/W',
					'pointable':   True,
					'overlayable': True, # thru flash mapping?
				},
			'code': {
					'address':     16,
					'read':        8,     # NOR flash can read 1 byte at a time
					'write':       16384, # 2KB page size as erase unit!
					'access':      'R',   # for all practical purpose
					'pointable':   True,
					'overlayable': True,  # thru SRAM mapping
				},
			# what about SFR, SBIT? Should they be considered here too?
			# how about address range, if more restricted than full range?
			# what about other qualifiers such as volatile?
			# or access method, such as var on stack?
			# or implicit addressing (address size = 0) e.g., DPTR?
			# or register?
			'register': {  # R0-R7
					'address':     3,  # 3 bits of pointer
					'read':        8,
					'write':       8,
					'access':      'R/W',
					'pointable':   False, # can't have a pointer to a register
					'overlayable': True,
				},

			'accumulator': {
					'address':     0,  # no pointer for accumulator
					'read':        8,
					'write':       8,
					'access':      'R/W',
					'pointable':   False,
					'overlayable': True,
				},

			'carrybit': {
					'address':     0,  # no pointer for C bit
					'read':        1,
					'write':       1,
					'access':      'R/W',
					'pointable':   False,
					'overlayable': True,
				},

			'DPTR': {
					'address':     0,  # no pointer for DPTR!
					'read':        16,
					'write':       16,
					'access':      'R/W',
					'pointable':   False,
					'overlayable': True,
				},

			'SFR16': {
					'address': 8,
					'read':    16,
					'write':   16,
					'access':  'R/W',
					'pointable': False,
					'overlayable': False,
				},

			'stackitem': {
					'address':     8,  # 8-bit offset from SP
					'read':        8,
					'write':       8,
					'access':      'R/W',
					'pointable':   True, # but dangerous...
					'overlayble':  True,
				},
		}


	def __init__(self, name, storageClass, varType, varAddress = None,
			mcu=None):
		'''constructor for CC2540VAR.
		  storageClass is a string: 'char', 'int', 'long', 'bool',
			'uint8', 'uint16', 'uint32', etc. perhaps even a bit field
			or a slice can also be a var?  Actually, the same
			multi-word C types can all be used.

			what if varAddress is left unspecified? it could be allocated
			automatically maybe?

			12/22/2013- extension to arrays, maybe also pointers.
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
					not (sizeInBits(varType[0]) in [8, 16]):
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

	def _readByte(self, storageClass, address):
		if storageClass in ['iram']:
			# use MOV instruction to read, but to where?
			# if it's a byte then read into A, but if bigger, then
			# maybe consecutive memory?
			self._emit('MOV A, 0x%x', address)
		elif storageClass in ['uram']:
			# use indirect MOV by putting address in R0
			self._emit('MOV R0, #0x%x', address)
			self._emit('MOV A, @R0')
		elif storageClass in ['xdata']:
			# use MOVX instruction to write
			self._emit('MOV DPTR, #0x%x', address)
			self._emit('MOVX A, @DPTR')
		elif storageClass in ['register']:
			# need register number...
			self._emit('MOV A, R%d', address)
		elif storageClass in ['stackitem']:
			# do indirect stack addressing with offset
			# assume we can use R0 or R1 for indirect addressing
			self._emit('MOV R%d, SP', 0)
			self._emit('ADD R%d, #%x', 0, address)
			self._emit('MOV A, @R0', address)
		# elif self._storageClass in ['code' ]: - can't be code
		else:
			# not a supported storage class
			raise TypeError('attempt to write to unsupported storage class %x'\
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
		code = CodeCapsule(self._mcu, dest)
		self._code = code
		# assume we always ahve read permission for now. later restrict
		if isinstance(self._varType, tuple):
			# this is an array type.
			# like C, we just load its address without checking bounds for now,
			# though later we could try to check it.
			# again, assume only external memory for now.
			self._emit('MOV R%d, #0x%x', 2, self._varAddress & 0xff)
			self._emit('MOV R%d, #0x%x', 3, (self._varAddress >> 8) & 0xff)
			code.setResultType(self._varType[0]+'*')
			return code
		size = self._typeDefn['size']
		code.setResultType(self._varType)
		if size == 1 and self._storageClass in ['bitMem']:
			if dest is None: dest=self._mcu.lookupVar('C')
			self._code = CodeCapsule(self._mcu, dest)
			# read bit into accumulator C -- this is the only allowed?
			# cannot allow multi-bit bitMem?
			self._emit('MOV C, 0x%x', self._varAddress)
			# somehow need to return a reference?? or assume C for now?
		elif size == 8:
			if dest is None: dest=self._mcu.lookupVar('A')
			self._code = CodeCapsule(self._mcu, dest)
			self._readByte(self._storageClass, self._varAddress)
		elif size == 16:
			self._code = CodeCapsule(self._mcu, self._mcu.lookupVar('R3R2'))
			# DPTR and XSP, plus a few SFR16s and XREG16
			if self._storageClass == 'SFR16':
				# put DPTR into R3:R2
				self._emit('MOV R%d, 0x%x', 2, self._varAddress[0])  # R2 = low byte
				self._emit('MOV R%d, 0x%x', 3, self._varAddress[1])  # R3 = high byte
			elif self.name() == 'R3R2':
				# nothing to do - already in R3R2
				pass
			elif self.name() == 'XSP':
				# read from its address (0x10 and 0x11 from XDATA)
				self._emit('MOV DPTR, #0x%x', 0x10)
				self._emit('MOVX A, @DPTR')
				self._emit('MOV R%d, A', 2)
				self._emit('INC DPTR')
				self._emit('MOVX A, @DPTR')
				self._emit('MOV R%d, A', 3)
			elif self._storageClass == 'XREG16':
				self._emit('MOV DPTR, #0x%x', self._varAddress)
				self._emit('MOV R%d, A', 2)
				self._emit('INC DPTR')
				self._emit('MOVX A, @DPTR')
				self._emit('MOV R%d, A', 3)
			else:
				raise TypeError('unsupported type %s for var read' % self._varType)

		else:
			raise Exception('reading variable of size %d not implemented' % size)

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
			self._code = CodeCapsule(self._mcu, dest=self)
		if self._storageClass in ['bitMem']:
			# need to check if 0 or 1.  If larger, throw exception!?
			# otherwise, use setb/clr (perhaps try to reuse SFR code?)
			# allowed type: bool, int, string of '0' or '1'
			if (value == True or value == 1 or value == '1'):
				self._emit('SETB 0x%x', self._varAddress)
			elif (value == False or value == 0 or value == '0'):
				self._emit('CLR 0x%x' % self._varAddress)
			elif isinstance(value, VAR) or isinstance(value, nrf2540sfr.SFR) \
					or isinstance(value, CodeCapsule):
				# RHS already called value.readSFR() or value.readVar();
				# in either case, the bit result is in C.
				# should check if size is same.
				self._emit('MOV 0x%x, C', self._varAddress)
				return self._code
			else:
				# too big to fit in bit! report error
				raise ValueError('cannot assign %s to bitMem' % value)
		# see if source is also a variable (of same size)
		if isinstance(value, nrf2540sfr.SFR) or isinstance(value, VAR) \
		  or isinstance(value, CodeCapsule):
			# assume 8 bit
			# Note that the runtime has already called value.readVar() or
			# value.readSFR()! in either case, RHS is in A, so
			# we just continue with code to write A to dest.
			# should check size.
			##### Writing a constant #####
			if self._storageClass in ['iram']:
				self._emit('MOV 0x%x, A', self._varAddress)
			elif self._storageClass in ['uram']:
				# need to load indirectly by putting address in R0
				self._emit('MOV R%d, #0x%x', 0, self._varAddress)
				self._emit('MOV @R%d, A', 0)
			elif self._storageClass in ['xdata']:
				# use MOVX instruction to write
				self._emit('MOV DPTR, # 0x%x, A', self._varAddress)
				self._emit('MOVX @DPTR, A')
			elif self._storageClass in ['register']:
				# need register number...
				self._emit('MOV R%d, A', self._varAddress)
			elif self._storageClass in ['DPTR']:
				# allow - only for 16-bit code capsule.
				if isinstance(value, nrf2540sfr.SFR):
					raise TypeError('cannot assign SFR to DPTR')
				# now var should be read already
				self._emit('MOV 0x%x, R%d', 0x83, 3) ## DPH
				self._emit('MOV 0x%x, R%d', 0x82, 2) ## DPL
				# was (incorrectly) self._emit('MOV DPTR, 0x%x', value)
			elif self._storageClass in ['stackitem']:
				# do indirect stack addressing with offset
				# assume we can use R0 or R1 for indirect addressing
				self._emit('MOV R0, SP')
				self._emit('MOV A, R%d', 0)
				self._emit('ADD A, #%x', self._varAddress)
				self._emit('XCH A, @R0')

			# elif self._storageClass in ['code' ]: - can't be code
			else:
				# not a supported storage class
				raise Exception('attempt to write to unsupported storage class %x'\
								% self._storageClass)

		elif isinstance(value, int):
			if not self._checkRange(value):
				raise ValueError('%s is out of range for %s' % (value,
						self._storageClass))
			##### Writing a constant #####
			if self._storageClass in ['iram']:
				# use MOV instruction to write
				# @@@ but depending on the byte width and endian, may need to
				# generate a sequence in case of writing literals,
				# or may call readVar into A in case of writing # var-to-var
				self._emit('MOV 0x%x, #0x%x', self._varAddress, value)
			elif self._storageClass in ['xdata']:
				# use MOVX instruction to write
				self._emit('MOV DPTR, #0x%x, A', self._varAddress)
				self._emit('MOVX @DPTR, #0x%x', value)
			elif self._storageClass in ['register']:
				# need register number...
				self._emit('MOV R%d, #0x%x', self._varAddress, value)
			elif self._storageClass in ['DPTR']:
				# just move literal.  Range check? should be within 64K
				if (value > 65535):
					raise ValueError('%s out of 16-bit range for DPTR' % value)
				self._emit('MOV DPTR, #0x%x', value)
			elif self._storageClass in ['stackitem']:
				# do indirect stack addressing with offset
				# assume we can use R0 or R1 for indirect addressing
				self._emit('MOV R0, SP')
				self._emit('MOV A, #0x%x', self._varAddress)
				self._emit('ADD A, R0')
				self._emit('MOV @R0, #0x%x', value)
			# elif self._storageClass in ['code' ]: - can't be code
			else:
				# not a supported storage class
				raise Exception('attempt to write to unsupported storage class %x'\
								% self._storageClass)
		else:
			raise Exception('writeVar does not support value %s' % value)

		# continue with code to write A to dest. conceptually
		# self._emit('MOV 0x%x, A', self._varAddress)
		return self._code

	def __repr__(self):
		return str(self.__class__.__name__+"('"+self._name+"')")

if __name__ == '__main__':
	g = globals()
	for varName in nRF24E1VAR._VAR.keys():
		defn = nRF24E1VAR._VAR[varName]
		storageClass = defn['storageClass']
		varType = defn['varType']
		varAddress = defn['varAddress']
		g[varName] = VAR(varName, storageClass, varType, varAddress)
	print nRF24E1VAR._VAR.keys()
