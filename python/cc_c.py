# cc_avr.py
# this is code capsule to generate C instead of assembly, then calling a compiler to compile to binary
# For now I'm using it to generate AVR code for the atmega2560, but I called it cc_c.py in the hopes that
# it can be more or less platform independent.
# Ideally, the only platform dependent parts should be the SFR definitions and a function to call the compiler

import os
from codecapsule import CodeCapsule
from isa_gcc import ISAGCC


typeDef = {
		'bool':           { 'size': 1,  'signed': False, 'align': False, 'ctype': 'bool'},
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

class CC_C(CodeCapsule):
	'''This is a code capsule that generates C. It should be compiled by the ISAGCC.
	'''
	_isa_constructor = ISAGCC

	def appendReturnValue(self):
		pass

	def getCode(self):
		'''Override getCode for generating C: only return the last emitted code'''
		return self._instructions[-1]

	def getCFunctionCode(self):
		return '''
			#include <stdint.h>
			#include <stdbool.h>
			%s foo() {
				return %s;
			}
			''' % (typeDef[self.getResultType()]['ctype'], self.getCode())

	def getAssemblyCode(self):
		tempfile = "CC_C_TMP"
		cfunction = self.getCFunctionCode()
		f = open(tempfile + '.c', 'w')
		f.write(cfunction)
		f.close()
		os.system('avr-gcc -mmcu=atmega2560 -S -O3 %s.c -o %s.s' % (tempfile, tempfile))
		f = open(tempfile + '.s', 'r')
		assemblycode = f.read()
		f.close()
		os.system('rm %s.c %s.s' % (tempfile, tempfile))
		return assemblycode

	def getMachineCode(self):
		'''Override getCode for generating C: call avr-gcc'''
		tempfile = "CC_C_TMP"
		cfunction = self.getCFunctionCode()
		f = open(tempfile + '.c', 'w')
		f.write(cfunction)
		f.close()
		os.system('avr-gcc -mmcu=atmega2560 -c -O3 %s.c -o %s.o' % (tempfile, tempfile))
		os.system('avr-objcopy --output-target=binary %s.o %s.bin' % (tempfile, tempfile))

		f = open(tempfile + '.bin', 'rb')
		binarycode = bytearray(f.read())
		f.close()
		os.system('rm %s.c %s.o %s.bin' % (tempfile, tempfile, tempfile))
		# Convert to a list of a list of normal ints, since codecapsule expects this
		return [[i for i in binarycode]]

	def __repr__(self):
		mode = self.reprMode()
		if mode == 'c':
			return self.getCFunctionCode()
		elif mode == 'asm':
			return self.getAssemblyCode()
		elif mode == 'text':
			return str(self.getCode())
		else:
			return CodeCapsule.__repr__(self)


	def unaryOperator(self, operator):
		# 20140225PC: how about changing CC_C to self.__class__
		# so that a subclass inheriting this method can call its
		# own constructor? will that work?
		code = CC_C(self._mcu, src=self)
		code.emit('%s(%s)' % (operator, self.getCode()))
		#TODONR
		code.setResultType(self.getResultType())
		return code

	def binaryOperator(self, other, operator):
		code = CC_C(self._mcu, src=self)
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
		elif isinstance(other, CodeCapsule):
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

	def __add__(self, other):
		return self.binaryOperator(other, '+')

	def __radd__(self, other):
		'''add is commutative, so handle with regular add
		   e.g., 1 + mcu.R2 handled as mcu.R2 + 1
		'''
		return self.__add__(other)

	def __sub__(self, other):
		return self.binaryOperator(other, '-')

	def __rsub__(self, other):
		'''
			sub is not commutative. simple way is to subtract and negate.
		'''
		return self.binaryOperator(other, '-').unaryOperator('-')

	def __and__(self, other):
		'''
			This is the bitwise AND operator.  Python does not allow the logical
			AND operator to be overridden.
		'''
		return self.binaryOperator(other, '&')

	def __rand__(self, other):  # This is commutative
		return self.__and__(other)

	def __or__(self, other):
		'''
			This is the bitwise OR operator.  Python does not allow the logical
			OR operator to be overridden.
		'''
		return self.binaryOperator(other, '|')

	def __ror__(self, other):
		return self.__or__(other)

	def __xor__(self, other):
		'''
			This is the bitwise OR operator.  Python does not allow the logical
			OR operator to be overridden.
		'''
		return self.binaryOperator(other, '^')

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
		# 20120204 PC: would it work to do it as 
		# self.binaryOperator(other, '+=') ??
		return self.binaryOperator(other, '+=')

	def __isub__(self, other):
		return self.binaryOperator(other, '-=')

	def __iand__(self, other):
		return self.binaryOperator(other, '&=')

	def __ior__(self, other):
		return self.binaryOperator(other, '|=')

	def __ixor__(self, other):
		return self.binaryOperator(other, '^=')

	def __imul__(self, other):
		return self.binaryOperator(other, '*=')

	def __idiv__(self, other):
		return self.binaryOperator(other, '/=')

	def __itruediv__(self, other):
		'''this is a placeholder for a //= b. placeholder for now.'''
		self.__truediv__(other)
		return self

	def __imod__(self, other):
		return self.binaryOperator(other, '%=')


	def __invert__(self):
		'''this is the bit-invert operator.'''
		return self.unaryOperator('~')

	def __neg__(self):
		'''this is the unary negation operator.'''
		return self.unaryOperator('-')

	# other operators include
	# __ipow__(self, other)
	def __ilshift__(self, other):
		return self.binaryOperator(other, '<<=')

	def __irshift__(self, other):
		return self.binaryOperator(other, '>>=')


	# __pos__(self)
	# __abs__(self)
	# __complex__(self)
	# __int__(self)
	# __long__(self)
	# __float__(self)


	def __eq__(self, other):
		return self.binaryOperator(other, '==')

	def __ne__(self, other):
		return self.binaryOperator(other, '!=')

	def __lt__(self, other):
		return self.binaryOperator(other, '<')

	def __le__(self, other):
		return self.binaryOperator(other, '<=')

	def __ge__(self, other):
		return self.binaryOperator(other, '>=')

	def __gt__(self, other):
		return self.binaryOperator(other, '>')

	def __mul__(self, other):
		return self.binaryOperator(other, '*')

	def __div__(self, other):
		return self.binaryOperator(other, '/')

	def __truediv__(self, other):
		pass

	def __floordiv__(self, other):
		return self.binaryOperator(other, '/')

	def __mod__(self, other):
		return self.binaryOperator(other, '%')

	def __divmod__(self, other):
		pass

	def __pow__(self, other, mod):
		# 20140224 PC -- really!?  ^ is xor
		return self.binaryOperator(other, '^')

	def __lshift__(self, other):
		return self.binaryOperator(other, '<<')

	def __rshift__(self, other):
		return self.binaryOperator(other, '>>')

	def __getitem__(self, index):
		'''this is self[index]. This works on pointer type, or
		   array type whose result is given as a pointer type
			 (so that the resultType string has a * in the end).
			 To do: should check range?
		'''
		# 20120224 PC: I think this is just a funny type of operator
		# of the format '(%s) [ %s ]' % (self.getCode(), index.getCode())
		# or something like that, right?
		t = self.getResultType()
		# if t[-1] == '*':
		elementType = t[:-1] # get rid of the pointer
		code = CC_C(self._mcu)
		code.emit('(%s)[%s]' % self.getCode(), str(index))
		code.setResultType(elementType)
		return code

	def __setitem__(self, index, value):
		'''this is self[index] = value.
		'''
		t = self.getResultType()
		elementType = t[:-1]
		code = CC_C(self._mcu)
		code.emit('(%s)[%s] = (%s)' % (self.getCode(), str(index), str(value)))
		return code


	def __call__(self, *param):
		'''this object is being *called* with the parameter.
		   we do the following code generation.
			 we need the ability to have recursive expressions
			 (i.e., function call as actual parameter)
			 To do: need to check param type against prototype???
		'''
		# generate code for passing parameters
		if param is None:
			paramListString = ''
		else:
			paramListString = ', '.join(map(str, param))
		code = CC_C(self._mcu)
		code.emit('%s(%s)' % (self.getCode(), paramListString))
		code.setResultType(self.getResultType()[:-2])
				# Note: a call has type of 'returnType()'
				# so, we just get rid of the '()' part of the type
		return code

