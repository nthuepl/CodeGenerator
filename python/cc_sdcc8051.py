# cc_sdcc8051.py
# this is code capsule to generate C instead of assembly,
# then calling a compiler to compile to binary
# this is based on Niels' cc_c.py.

import os
from cc_c import CC_C
import isa_8051
# strictly speaking, isa_gcc is really generic and doesn't have to be
# tied to gcc at all.


typeDef = {
		'bool':           { 'size': 1,  'signed': False, 'align': False, 'ctype': 'bool'},
		'bit':           { 'size': 1,  'signed': False, 'align': False, 'ctype': 'bool'},
		'bitMem':           { 'size': 1,  'signed': False, 'align': False, 'ctype': 'bool'},
		'char':           { 'size': 8,  'signed': True,  'align': False, 'ctype': 'int8_t'},
		'char':           { 'size': 8,  'signed': True,  'align': False, 'ctype': 'int8_t'},
		'unsigned char':  { 'size': 8,  'signed': False, 'align': False, 'ctype': 'uint8_t'},
		'uint8':          { 'size': 8,  'signed': False, 'align': False, 'ctype': 'uint8_t'},
		'int8':           { 'size': 8,  'signed': True,  'align': False, 'ctype': 'int8_t'},
		'short':          { 'size': 16, 'signed': True,  'align': True,  'ctype': 'int16_t'},
		'unsigned short': { 'size': 16, 'signed': False, 'align': True,  'ctype': 'uint16_t'},
		'uint16':         { 'size': 16, 'signed': False, 'align': True,  'ctype': 'uint16_t'},
		'uint32':         { 'size': 32, 'signed': False, 'align': True,  'ctype': 'uint32_t'},
		'int32':          { 'size': 32, 'signed': True,  'align': True,  'ctype': 'int32_t'},
		'char*':          { 'size': 32, 'signed': False, 'align': True,  'ctype': 'int8_t*'},
		'int8*':          { 'size': 32, 'signed': False, 'align': True,  'ctype': 'int8_t*'},
		'uint8*':         { 'size': 32, 'signed': False, 'align': True,  'ctype': 'uint8_t*'},
		'uint16*':        { 'size': 32, 'signed': False, 'align': True,  'ctype': 'uint16_t*'},
		'int32*':         { 'size': 32, 'signed': False, 'align': True,  'ctype': 'int32_t*'},
		'uint32*':        { 'size': 32, 'signed': False, 'align': True,  'ctype': 'uint32_t*'},
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
	if not inRange(value, bits, signed):
		raise ValueError('%d-bit constant value %s out of range: should be %d..%d' \
					% (bits, value, lower, upper))

def inRange(value, bits, signed): # > 65535 or other < -32768):
	if signed:
		# value should be between -2^(n-1) and 2^(n-1) - 1
		lower = -(1 << (bits - 1))
		upper = (1 << (bits - 1)) - 1
	else:
		# value should be between 0 and 2^(n) - 1
		lower = 0
		upper = (1 << bits) - 1
	return (value > lower) and (value < upper)


def getType(bits, signed):
	return [t for t in typeDef.keys() if typeDef[t]['size'] == bits and typeDef[t]['signed'] == signed][0]

def determineTypeForConstantInt(value):
	signed = (value < 0)
	if (inRange(value, 1, signed)):
		bits = 1
	elif (inRange(value, 8, signed)):
		bits = 8
	elif (inRange(value, 16, signed)):
		bits = 16
	elif (inRange(value, 32, signed)):
		bits = 32
	else:
		raise ValueError('No type large enough to hold %d' % value)
	return getType(bits, signed)

def determineResultType(type1, type2):
	'''
	Determine the resulttype of an expression from the operand types.
	Not really sure what to do in some cases. Need to revisit this later.
	'''
	if type1 == type2:
		return type1
	if type1[-1] == '*' or type2[-1] == '*':
		raise ValueError("Can't do pointer arithmetic.")
	size = max(typeDef[type1]['size'], typeDef[type2]['size'])
	signed = typeDef[type1]['signed'] or typeDef[type2]['signed']
	return getType(size, signed)

class CC_SDCC8051(CC_C):
	'''This is a code capsule that generates C. It should be compiled by the 
	   SDCC for 8051. It inherits from Niels's CC_C (code capsule for C)
	'''
	# inherit the following:
	# _isa_constructor = ISAGCC
	# appendReturnValue()
	# getCode()



	def getCFunctionCode(self):
		'''This should be upgraded to parameterize include files'''
		resultType = typeDef[self.getResultType()]['ctype']
		if resultType == 'bool':
			# boolean has to be stored at a byte address
			resultType = 'uint8'
		return '''
#include <%ssfr.h>
#include <sdcctype.h>
#include <stdint.h>
#include <stdbool.h>
__xdata __at (0x%x) %s retbuf;
void foo() {
				retbuf = %s;
}
			''' % (self._mcu._chipName, self._mcu.getReturnBufferAddress(), resultType, self.getCode())

	def getAssemblyCode(self):
		tempfile = "CC_C_TMP"
		cfunction = self.getCFunctionCode()
		f = open(tempfile + '.c', 'w')
		f.write(cfunction)
		f.close()
		os.system('sdcc --model-small -mmcs51 --Werror -I. --iram-size 0x100 --code-size 0x1000 --code-loc 0x0000 --stack-loc 0x30 --data-loc 0x30 --out-fmt-ihx -c %s.c' % tempfile)
		f = open(tempfile + '.asm', 'r')
		assemblycode = f.read()
		f.close()
		os.system('rm %s' % ' '.join(map(lambda x: tempfile+'.'+x, ['asm', 'ihx', 'lk', 'lst', 'map', 'mem', 'rel', 'rst', 'sym'])))
		return assemblycode

	def getMachineCode(self):
		'''Override getCode for generating C: call sdcc 8051'''
		tempfile = "CC_C_TMP"
		cfunction = self.getCFunctionCode()
		f = open(tempfile + '.c', 'w')
		f.write(cfunction)
		f.close()
		os.system('sdcc --model-small -mmcs51 --Werror -I. --iram-size 0x100 --code-size 0x1000 --code-loc 0x0000 --stack-loc 0x30 --data-loc 0x30 --out-fmt-ihx -c %s.c' % tempfile)
		os.system('sdcc --model-small -mmcs51 --Werror -I. --iram-size 0x100 --code-size 0x1000 --code-loc 0x0000 --stack-loc 0x30 --data-loc 0x30 --out-fmt-ihx %s.rel' % tempfile)
		# os.system('packihx %s.ihx > %s.hex' % (tempfile, tempfile))
		os.system('sdobjcopy --input-target=ihex --output-target=binary %s.ihx %s.bin' % (tempfile, tempfile))

		f = open(tempfile + '.bin', 'rb')
		binarycode = bytearray(f.read())
		f.close()
		os.system('rm %s' % ' '.join(map(lambda x: tempfile+'.'+x, ['asm', 'ihx', 'lk', 'lst', 'map', 'mem', 'rel', 'rst', 'sym'])))
		# Convert to a list of a list of normal ints, since codecapsule expects this
		return [[i for i in binarycode]]

	def __repr__(self):
		mode = self.reprMode()
		if mode == 'c':
			return self.getCFunctionCode()
		elif mode == 'asm':
			return self.getAssemblyCode()
		elif mode == 'disasm':
			# flatten the machine code then disassemble
			m = self.getMachineCode()
			#print 'machine code is', m
			m = reduce(lambda x,y:x+y, m)
			#print 'reduced machine code is', m
			m = isa_8051.disasm(m)
			#print 'disassembled code is', m
			return m
		elif mode == 'text':
			return str(self.getCode())
		else:
			return CC_C.__repr__(self)


	def unaryOperator(self, operator):
		code = CC_SDCC8051(self._mcu, src=self)
		code.emit('%s(%s)' % (operator, self.getCode()))
		#TODONR
		code.setResultType(self.getResultType())
		return code

	def binaryOperator(self, other, operator):
		code = CC_SDCC8051(self._mcu, src=self)
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
			otherAsString = str(other)
			otherType = determineTypeForConstantInt(other)
		elif isinstance(other, CC_C):
			otherAsString = other.getCode()
			otherType = other.getResultType()
		else:
			raise TypeError('unsupported type for +: %s' % type(other))
		code.emit('(%s) %s (%s)' % (self.getCode(), operator, otherAsString))
		if operator in ['>', '>=', '==', '!=', '<=', '<']:
			# Comparison, result will be a boolean
			code.setResultType('bool')
		else:
			code.setResultType(determineResultType(self.getResultType(), otherType))
		return code

	# inherit
	# __add__
	# __radd__
	# __sub__
	# __rsub__
	# __and__
	# __rand__
	# __or__
	# __ror__
	# __xor__
	# __rxor__
	# __iadd__
	# __isub__
	# __iand__
	# __ior__
	# __ixor__
	# __imul__
	# __idiv__
	# __itruediv__
	# __imod__
	# __invert__
	# __neg__
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


	# __eq__
	# __ne__
	# __lt__
	# __le__
	# __ge__
	# __gt__
	# __mul__
	# __div__
	# __truediv__
	# __floordiv__
	# __mod__
	# __divmod__
	# __pow__
	# __lshift__
	# __rshift__
	# __getitem__
	# __setitem__
