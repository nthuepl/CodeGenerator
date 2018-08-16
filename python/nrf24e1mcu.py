'''
  This is the top-level MCU class for the nRF24E1. 
	It is modified based on CC2540MCU.
  The user of this class should actually define variables using
	defVar() method, and use addresses outside register space 
	(0x00 - 0x1f).  interactive execution lets you see the code
	generated.

	1/8/2014 -it is not working yet.
'''
import nrf24e1sfr
import nrf24e1var
from sdcc8051 import MapFile, API # this is the mapfile

class nRF24E1MCU:
	def __init__(self):
		'''constructor. make memory, add sfr'''
		self.sfrDict = { }
		# make an SFR instance 
		for sfrName in nrf24e1sfr.nRF24E1SFR._SFR.keys():
			self.sfrDict[sfrName] = nrf24e1sfr.SFR(sfrName, self)

		self.varDict = { }
		for varName in nrf24e1var.nRF24E1VAR._VAR.keys():
			# read out standard variables and registers and make constructors
			defn = nrf24e1var.nRF24E1VAR._VAR[varName]
			storageClass = defn['storageClass']
			varType = defn['varType']
			varAddress = defn['varAddress']
			self.defVar(varName, storageClass, varType, varAddress)

		self.__dict__['_tempsAvail'] = [ \
				self.varDict['R7'],
				self.varDict['R6'],
				self.varDict['R5'],
				self.varDict['R4'],
				self.varDict['R3'],
				self.varDict['R2'],
			]
		self.__dict__['_tempsInUse'] = [ ]

		self.__dict__['_tempBitsAvail'] = [ \
				self.varDict['tempBit0'],
				self.varDict['tempBit1'],
				self.varDict['tempBit2'],
				self.varDict['tempBit3'],
				self.varDict['tempBit4'],
				self.varDict['tempBit5'],
				self.varDict['tempBit6'],
				self.varDict['tempBit7'],
			]

		self.__dict__['_tempBitsInUse'] = [ ]

		self.__dict__['_mapAPI'] = MapFile._map
		for fnName in self._mapAPI.keys():
			# instantiate
			if self.__dict__.has_key(fnName):
				raise NameError('function name %s duplicates existing symbol' \
						% fnName)
			self.__dict__[fnName] = API(fnName, self)
		self.__dict__['_bufAddress'] = 0x0028 ## @@@ should be changed
		self.__dict__['_reprMode'] = 'text'  # either text or binary
		self.__dict__['_appendReturnBuf'] = True

	def setReprMode(self, mode):
		self.__dict__['_reprMode'] = mode

	def reprMode(self):
		return self.__dict__['_reprMode']

	def getReturnBufferAddress(self):
		'''This is a method for the address for the return value,
		   in order to return back to the user
		'''
		return self.__dict__['_bufAddress']

	def setReturnBufferAddress(self, address):
		'''This is a method for setting the return buffer address'''
		self.__dict__['_bufAddress'] = address

	def setAppendReturnBufCode(self, mode):
		'''mode = True to append the return buffer code in CodeCapsule's __repr__,
		   so that it writes the length byte starting _bufAddress, followed by the
			 data; 
		   mode = False to disable appending this code.
		'''
		self._appendReturnBuf = mode

	def getAppendReturnBufCode(self):
		'''return True for appending return-buffer code in CodeCapsule's __repr__,
		   False for not appending.
		'''
		return self._appendReturnBuf


	def allocTemp(self, temp=None):
		'''allocate a free temp from the pool'''
		if len(self._tempsAvail) == 0:
			raise IndexError('No more temporary registers to allocate')
		if (temp is None):
			ret = self._tempsAvail.pop() # remove from end
		else:
			# look up by name and pop
			t = self.varDict[temp]
			# allocate the designated one
			ret = self._tempsAvailable.remove(t)
			# if not in list, let it throw an exception
		self._tempsInUse.append(ret) # add to end
#		print 'alloc %s: avail=%s, inuse=%s' % (ret.name(),
#				self._tempsAvail, self._tempsInUse)
		return ret

	def freeTemp(self, obj):
		'''put an allocated temp back into the free pool'''
		if not obj in self._tempsInUse:
			raise ValueError("freeTemp(%s) not a temp in use!" % obj)
		self._tempsInUse.remove(obj)
		self._tempsAvail.append(obj)
#		print 'free %s: avail=%s, inuse=%s' % (obj.name(),
#				self._tempsAvail, self._tempsInUse)


	def allocTempBit(self, temp=None):
		'''allocate a free temp bit from the pool'''
		if len(self._tempBitsAvail) == 0:
			raise IndexError('No more temporary bits to allocate')
		if (temp is None):
			ret = self._tempBitsAvail.pop() # remove from end
		else:
			# look up by name and pop
			t = self.varDict[temp]
			# allocate the designated one
			ret = self._tempBitsAvailable.remove(t)
			# if not in list, let it throw an exception
		self._tempBitsInUse.append(ret) # add to end
		return ret

	def freeTempBit(self, obj):
		'''put an allocated temp bit back into the free pool'''
		if not obj in self._tempBitsInUse:
			raise ValueError("freeTempBit(%s) not a temp in use!" % obj)
		self._tempBitsInUse.remove(obj)
		self._tempBitsAvail.append(obj)
#		print 'free %s: avail=%s, inuse=%s' % (obj.name(),
#				self._tempsAvail, self._tempsInUse)

	def lookupVar(self, name):
		return self.varDict[name]

	def defVar(self, varName, storageClass, varType, varAddress):
		'''user code to define a variable of given type at given address.
		  - varName is any valid identifier
			- storageClass is bitMem (no byteMem?)
			  - could be register!?
			  - byteMem?
			  - DPTR
			- varType 
			  - bool,  
			  - char,  - unsigned char,  - uint8,
			  - short, - unsigned short, - uint16,
			  - long,  - unsigned long,  - uint32
		'''
		newVar = nrf24e1var.VAR(varName, storageClass, varType, varAddress,
				self)
		self.varDict[varName] = newVar
		return newVar


	def __getattr__(self, name):
		'''mcu.sfr. Treated as a get value from the MCU's SFR.
		   returns a code capsule for generating the read.
		'''
		if self.sfrDict.has_key(name):
			s = self.sfrDict[name]
			if isinstance(s, nrf24e1sfr.SFR):
				return s.readSFR()  # do an actual load, rather than cached value
			else:
				raise TypeError('%s is not an instance of nRF24E1.SFR' % s)
		elif self.varDict.has_key(name):
			s = self.varDict[name]
			if isinstance(s, nrf24e1var.VAR):
				return s.readVar()
		raise AttributeError('name %s not an attribute of MCU' % name)

	def __setattr__(self, name, value):
		'''mcu.sfr. Treat as a write to MCU's SFR.'''
		if self.__dict__.has_key(name) or  \
				not self.__dict__.has_key('sfrDict') and name=='sfrDict' or  \
				not self.__dict__.has_key('varDict') and name=='varDict':
			self.__dict__[name] = value
		else:
			sfrDict = self.__dict__['sfrDict']
			if sfrDict.has_key(name):
				s = sfrDict[name]
				if isinstance(s, nrf24e1sfr.SFR):
					print s.writeSFR(value)
					return
			else:
				varDict = self.__dict__['varDict']
				s = varDict[name]
				if isinstance(s, nrf24e1var.VAR):
					print s.writeVar(value)
					return
			raise TypeError('%s is not an instance of nrf24e1.SFR' % s)



if __name__ == '__main__':
	# make an instance to see if it works
	mcu = nRF24E1MCU()
	# (varName, storageClass, varType, varAddress):
	varList = [ \
			('i0', 'iram', 'uint8', 0x40),
			('i1', 'iram', 'uint8', 0x41),
			('i2', 'iram', 'uint8', 0x42),
			('i3', 'iram', 'uint8', 0x43),
			('i4', 'iram', 'uint8', 0x44),
			('i5', 'iram', 'uint8', 0x45),
			('i6', 'iram', 'uint8', 0x46),
			('i7', 'iram', 'uint8', 0x47),
			('u0', 'uram', 'uint8', 0xc0),
			('u1', 'uram', 'uint8', 0xc1),
			('u2', 'uram', 'uint8', 0xc2),
			('u3', 'uram', 'uint8', 0xc3),
			('u4', 'uram', 'uint8', 0xc4),
			('u5', 'uram', 'uint8', 0xc5),
			('u6', 'uram', 'uint8', 0xc6),
			('u7', 'uram', 'uint8', 0xc7),
			('b0', 'bitMem', 'bool', 0x0),
			('b1', 'bitMem', 'bool', 0x1),
			('b2', 'bitMem', 'bool', 0x2),
			('b3', 'bitMem', 'bool', 0x3),
			('b4', 'bitMem', 'bool', 0x4),
			('b5', 'bitMem', 'bool', 0x5),
			('b6', 'bitMem', 'bool', 0x6),
			('b7', 'bitMem', 'bool', 0x7),
			]
	map(lambda x: apply(mcu.defVar, x), varList)