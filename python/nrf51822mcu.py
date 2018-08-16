'''
  This is the top-level MCU class. 
	see the test case below for example.
	instantiate the nRF51822MCU (no argument in constructor, at least for
	now) and it will create all the SFRs and "Vars" (but these are just
	registers for testing).
  The user of this class should actually define variables using
	defVar() method.
	interactive execution lets you see the code generated.
'''
import nrf51822sfr
import nrf51822var
from gccarm import MapFile, API # mapfile

class nRF51822MCU:
	def __init__(self):
		'''constructor. make memory, add sfr'''
		# do the XREG first, then SFR version overwrite them if available.
		self.sfrDict = { }
		# make an SFR instance 
		for sfrName in nrf51822sfr.nRF51822SFR._SFR.keys():
			self.sfrDict[sfrName] = nrf51822sfr.SFR(sfrName, self)

		self.varDict = { }
		for varName in nrf51822var.nRF51822VAR._VAR.keys():
			# read out standard variables and registers and make constructors
			defn = nrf51822var.nRF51822VAR._VAR[varName]
			storageClass = defn['storageClass']
			varType = defn['varType']
			varAddress = defn['varAddress']
			self.defVar(varName, storageClass, varType, varAddress)


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

	# no longer using allocTemp for Thumb
	# def allocTemp(self, temp=None):

	# no longer using freeTemp for Thumb
	# def freeTemp(self, obj):

	# no longer using allocTempBit for Thumb
	# def allocTempBit(self, temp=None):

	# no longer using freeTempBit for Thumb
	# def freeTempBit(self, obj):

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
		newVar = nrf51822var.VAR(varName, storageClass, varType, varAddress,
				self)
		self.varDict[varName] = newVar
		return newVar


	def __getattr__(self, name):
		'''mcu.sfr. Treated as a get value from the MCU's SFR.
		   returns a code capsule for generating the read.
		'''
		if self.sfrDict.has_key(name):
			s = self.sfrDict[name]
			if isinstance(s, nrf51822sfr.SFR):
				return s.readSFR()  # do an actual load, rather than cached value
			else:
				raise TypeError('%s is not an instance of cc2540.SFR' % s)
		elif self.varDict.has_key(name):
			s = self.varDict[name]
			if isinstance(s, nrf51822var.VAR):
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
				if isinstance(s, nrf51822sfr.SFR):
					print s.writeSFR(value)
					return
			else:
				varDict = self.__dict__['varDict']
				s = varDict[name]
				if isinstance(s, nrf51822var.VAR):
					print s.writeVar(value)
					return
			raise TypeError('%s is not an instance of nrf51822sfr.SFR' % s)



if __name__ == '__main__':
	# make an instance to see if it works
	mcu = nRF51822MCU()
	# (varName, storageClass, varType, varAddress):
	varList = [ \
			('a0', 'xdata', ('uint8', 12), 0x100),
			('a1', 'xdata', ('uint8', 12), 0x110),
			('s0', 'xdata', 'uint16', 0x200),
			('s1', 'xdata', 'uint16', 0x202),
			('s2', 'xdata', 'uint16', 0x204),
			]
	map(lambda x: apply(mcu.defVar, x), varList)