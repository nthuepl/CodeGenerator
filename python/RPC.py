# this is a dummy RPC.py 
# for local testing 

import struct

def call(code, retVal):
	# algorithm: send code to node
	# now return result
	return retVal

typeMap = {
		'char': ('s', 1),
		'signed char': ('s', 1),
		'int8': ('b', 1),
		'uint8': ('B', 1),
		'int16': ('<h', 2),
		'uint16': ('<H', 2),
		'int': ('<i', 4),
		'int32': ('<i', 4),
		'uint32': ('<I', 4),
		'void': ('x', 0),
		'bool': ('?', 1),
}

def demarshal(data, toType):
	if toType == 'void':
		return None
	if not typeMap.has_key(toType):
		raise TypeError('unknown result type %s' % toType)
	fmt, length = typeMap[toType]
	return struct.unpack(fmt, data[:length])[0]
