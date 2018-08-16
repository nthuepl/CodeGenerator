'''
   This is an attempt to build up variables for ATMEGA2560
	 I suppose a lot of it could be extracted out to a common 8051 set,
	 but let's stick to ATMEGA2560 because it has a few nice features such
	 as multiple DPTRs.

	 Let's start with just simple byte variables at first, though we can
	 also do int (16 bit) -- necessary for addresses, long (32 bit), etc.
   we'll add array, struct, and pointers later.

	 Usage: the user creates a variable on the ATMEGA2560 (MCU?),
	 possibly by naming convention or by assignment?  or by
	 calling a "factory" to allocate or free a variable?
	 Actually, before full variables, we may also need temporary
	 variables, which may be mapped to stack or register access.

	 In 8051, variables need to have an associated storage class.
'''
import atmega2560sfr
from cc_avr import CC_AVR as CodeCapsule
from cc_avr import typeDef
import cc_avr

class ATMEGA2560VAR:
	'''
		this is the class for variables in ATMEGA2560.
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
			'R8': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 8, },
			'R9': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 9, },
			'R10': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 10, },
			'R11': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 11, },
			'R12': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 12, },
			'R13': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 13, },
			'R14': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 14, },
			'R15': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 15, },
			'R16': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 16, },
			'R17': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 17, },
			'R18': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 18, },
			'R19': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 19, },
			'R20': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 20, },
			'R21': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 21, },
			'R22': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 22, },
			'R23': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 23, },
			'R24': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 24, },
			'R25': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 25, },
			'R26': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 26, },
			'R27': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 27, },
			'R28': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 28, },
			'R29': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 29, },
			'R30': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 30, },
			'R31': { 'storageClass': 'register', 'varType': 'uint8',
						'varAddress': 31, },

			'DPTR': { 'storageClass': 'SFR16', 'varType': 'uint16',
						'varAddress': [0x82, 0x83], }, # DPL, DPH
			'ADC': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0xBA, 0xBB], }, # ADCL, ADCH
			'RND': { 'storageClass': 'SFR16', 'varType': 'uint16',
				'varAddress': [0xBC, 0xBD], }, # RNDL, RNDH
			'DMA0CFG': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xD4, 0xD5],  # DMA1CFGL, DMA1CFGH
				},
			'DMA1CFG': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xD2, 0xD3],  # DMA1CFGL, DMA1CFGH
				},
			'T1CC0': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xDA, 0xDB], 
				},
			'T1CC1': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xDC, 0xDD],
				},
			'T1CC2': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xDE, 0xDF],
				},
			'T1CNT': { 'storageClass': 'SFR16', 'varType': 'uint16',
					'varAddress': [0xE2, 0xE3],
				},
			'USBFRM': { 'storageClass': 'XREG16', 'varType': 'uint16',
					'varAddress': 0x620C,
				},
			##### IAR's XDATA emulated stack for local data and parameters ###
			'XSP': { 'storageClass': 'xdata', 'varType': 'uint16',
						'varAddress': 0x10, },
			#### The following are IAR's parameter registers ####
			'B_0': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf0, },
			'B_1': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf1 },
			'B_2': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf2 },
			'B_3': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf3 },
			'B_4': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf4 },
			'B_5': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf5 },
			'B_6': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf6 },
			'B_7': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0xf7 },
			'VB_0': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x00, },
			'VB_1': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x01, },
			'VB_2': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x02, },
			'VB_3': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x03, },
			'VB_4': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x04, },
			'VB_5': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x05, },
			'VB_6': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x06, },
			'VB_7': { 'storageClass': 'bitMem', 'varType': 'bool',
					'varAddress': 0x07, },
			 #### We don't support VB register -- what is it!? ####
			 'R3R2': { 'storageClass': 'register', 'varType': 'uint16',
				 'varAddress': [0x3, 0x2] },
			 'R5R4': { 'storageClass': 'register', 'varType': 'uint16',
				 'varAddress': [0x5, 0x4] },
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
	return cc_avr.sizeInBits(typeName)

def isSigned(typeName):
	return cc_avr.isSigned(typeName)



class VAR:
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

			'XREG16': {
					'address': 16,
					'read':    16,
					'write':   16,
					'access':  'R/W',
					'pointable': True,
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
		'''constructor for ATMEGA2560VAR.
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
			if not typeDef.has_key(varType[0]) or \
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
			self._typeDefn     = typeDef[varType[0]]
		elif not typeDef.has_key(varType):
			raise TypeError('var %s of type %s not supported' % (name,varType))
		else:
			# this is one of the basic types.
			self._typeDefn     = typeDef[varType]
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
		if storageClass == 'iram':
			# use MOV instruction to read, but to where?
			# if it's a byte then read into A, but if bigger, then
			# maybe consecutive memory?
			self._emit('MOV A, 0x%x', address)
		elif storageClass == 'uram':
			# use indirect MOV by putting address in R0
			self._emit('MOV R0, #0x%x', address)
			self._emit('MOV A, @R0')
		elif storageClass == 'xdata':
			# use MOVX instruction to write
			self._emit('MOV DPTR, #0x%x', address)
			self._emit('MOVX A, @DPTR')
		elif storageClass == 'register':
			# need register number...
			self._emit('MOV A, R%d', address)
		elif storageClass == 'stackitem':
			# do indirect stack addressing with offset
			# assume we can use R0 or R1 for indirect addressing
			self._emit('MOV R%d, SP', 0)
			self._emit('ADD R%d, #%x', 0, address)
			self._emit('MOV A, @R0', address)
		# elif self._storageClass in ['code' ]: - can't be code
		elif storageClass == 'bitMem':
			self._emit('MOV C, 0x%x', address)
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
			self._code = code
			# read bit into accumulator C -- this is the only allowed?
			# cannot allow multi-bit bitMem?
			self._emit('MOV C, 0x%x', self._varAddress)
			# somehow need to return a reference?? or assume C for now?
		elif size == 8:
			if dest is None: dest=self._mcu.lookupVar('A')
			self._code = code
			self._readByte(self._storageClass, self._varAddress)
		elif size == 16:
			# self._code = CodeCapsule(self._mcu, self._mcu.lookupVar('R3R2'))
			self._code = code
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
			if (value == True) or (value == 1):
				self._emit('SETB 0x%x', self._varAddress)
			elif (value == False) or (value == 0):
				self._emit('CLR 0x%x', self._varAddress)
			elif isinstance(value, VAR) or isinstance(value, atmega2560sfr.SFR) \
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
		if isinstance(value, atmega2560sfr.SFR) or isinstance(value, VAR) \
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
				if isinstance(value, atmega2560sfr.SFR):
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

		elif isinstance(value, int) or isinstance(value, str):
			if isinstance(value, str):
				if len(value) == 0:
					value = 0
				elif len(value) == 1:
					value = ord(value)
				else:
					raise ValueError('cannot write string %s to var %s' % (value,
						self._name))
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
				raise Exception('attempt to write to unsupported storage class %s'\
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
	for varName in ATMEGA2560VAR._VAR.keys():
		defn = ATMEGA2560VAR._VAR[varName]
		storageClass = defn['storageClass']
		varType = defn['varType']
		varAddress = defn['varAddress']
		g[varName] = VAR(varName, storageClass, varType, varAddress)
	print ATMEGA2560VAR._VAR.keys()
