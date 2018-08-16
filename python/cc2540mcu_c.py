'''
  This is the top-level cc2540 MCU class, using SDCC for code
	generation.  It will eventually replace the original cc2540mcu.py
	class.  Also, due to the restructuring of class files, it will no
	longer be necessary to use an SFR class that is specific to cc2540
	(since the definition is extracted out); instead, it will use a
	shared class for SDCC 8051 for code.  Ideally, we can mix and match
	these classes for different compilers and MCUs of the same ISA.

	instantiate the CC2540MCU (no argument in constructor, at least for
	now) and it will create all the SFRs and "Vars" (but these are just
	registers for testing).
  The user of this class should actually define variables using
	defVar() method, and use addresses outside register space 
	(0x00 - 0x1f).  interactive execution lets you see the code
	generated.
'''
import cc2540sfr_c
import cc2540var
import CodeGenerator
from mapfile import MapFile, API
from sdcc8051sfr import SFR


class CC2540MCU:
	_chipName = 'cc2540'

	def __init__(self, CG = None):
		'''constructor. make memory, add sfr'''
		# do the XREG first, then SFR version overwrite them if available.
		self.__dict__['CG'] = CG
		self.sfrDict = { }
		c = cc2540sfr_c.CC2540SFR()
		for sfrName in c._XREG.keys():
			self.sfrDict[sfrName] = SFR(sfrName, c._XREG[sfrName], self)
		# make an SFR instance 
		for sfrName in c._SFR.keys():
			self.sfrDict[sfrName] = SFR(sfrName, c._SFR[sfrName], self)

		self.varDict = { }
		for varName in cc2540var.CC2540VAR._VAR.keys():
			# read out standard variables and registers and make constructors
			defn = cc2540var.CC2540VAR._VAR[varName]
			storageClass = defn['storageClass']
			varType = defn['varType']
			varAddress = defn['varAddress']
			self.defVar(varName, storageClass, varType, varAddress)

		self.__dict__['_tempsAvail'] = [ \
				self.varDict['R2'],
				self.varDict['R3'],
				self.varDict['R4'],
				self.varDict['R5'],
				self.varDict['R6'],
				self.varDict['R7'],
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
		duplicated = [ ]
		for fnName in self._mapAPI.keys():
			# instantiate
			if self.sfrDict.has_key(fnName) or self.varDict.has_key(fnName) or \
					self.__dict__.has_key(fnName):
				duplicated.append(fnName)
			else:
				self.__dict__[fnName] = API(fnName, self)
		if duplicated:
			print 'duplicated mapfile names: ', duplicated
		self.__dict__['_bufAddress'] = 0x0881 ## @@@ should be changed
		self.__dict__['_reprMode'] = 'text'  # either text or binary
		self.__dict__['_appendReturnBuf'] = True
	
	def send(self, code, retval_type):
		return self.__dict__['CG'].send(code, retval_type=retval_type)

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
		newVar = cc2540var.VAR(varName, storageClass, varType, varAddress,
				self)
		self.varDict[varName] = newVar
		return newVar


	def __getattr__(self, name):
		'''mcu.sfr. Treated as a get value from the MCU's SFR.
		   returns a code capsule for generating the read.
		'''
		if self.sfrDict.has_key(name):
			s = self.sfrDict[name]
			if isinstance(s, SFR):
				return s.readSFR()  # do an actual load, rather than cached value
			else:
				raise TypeError('%s is not an instance of SFR' % s)
		elif self.varDict.has_key(name):
			s = self.varDict[name]
			if isinstance(s, cc2540var.VAR):
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
				if isinstance(s, SFR):
					print s.writeSFR(value)
					return
			else:
				varDict = self.__dict__['varDict']
				s = varDict[name]
				if isinstance(s, cc2540var.VAR):
					print s.writeVar(value)
					return
			raise TypeError('%s is not an instance of SFR' % s)



if __name__ == '__main__':
	# make an instance to see if it works
	CG = None
	UseSerialPort = False
	if UseSerialPort:
		com_dic = CodeGenerator.scan_com_port()

		print "Available COM ports"
		for x in range(len(com_dic)):
			print str(x+1)+": "+com_dic[x+1]
	
		port = com_dic[int(raw_input("Select COM port: "))]
		CG = CodeGenerator.CodeGen(port)
		nodeNumber = int(raw_input("Select node: "))
		CG.connect(nodeNumber)
	
	mcu = CC2540MCU(CG)
	# (varName, storageClass, varType, varAddress):
	varList = [ \
			('i0', 'iram', 'uint8', 0x40),
			('i1', 'iram', 'char', 0x41),
			('i2', 'iram', 'uint8', 0x42),
			('i3', 'iram', 'uint8', 0x43),
			('i4', 'iram', 'uint8', 0x44),
			('i5', 'iram', 'uint8', 0x45),
			('i6', 'iram', 'uint8', 0x46),
			('i7', 'iram', 'uint8', 0x47),
			('u0', 'uram', 'uint8', 0xc0),
			('u1', 'uram', 'char', 0xc1),
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
			('a0', 'xdata', ('uint8', 12), 0x100),
			('a1', 'xdata', ('uint8', 12), 0x110),
			('s0', 'xdata', 'uint16', 0x200),
			('s1', 'xdata', 'uint16', 0x202),
			('s2', 'xdata', 'uint16', 0x204),
			]
	map(lambda x: apply(mcu.defVar, x), varList)