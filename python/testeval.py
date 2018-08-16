# testeval.py
# test the evaluation order of operators

class Port:
	def __init__(self, name):
		self.name = name

	def readVal(self):
		print "readVal %s" % self.name
		return self

	def writeVal(self, val):
		print "writeVal %s = %s" % (self.name, val)
		return self

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self.name)

	def __add__(self, other):
		print "+ %s %s" % (self.name, other.name)
		return self


class Mcu:
	def __init__(self):
		ports = ['P0', 'P1', 'P2', 'P3', 'R0', 'R1', 'R2', 'R3', 'R4',
			'R5', 'R6', 'R7']
		self.__dict__['portDict'] = {}
		for p in ports:
			self.portDict[p] = Port(p)

	def __getattr__(self, name):
		if self.portDict.has_key(name):
			return self.portDict[name].readVal()
		raise NameError("%s not in Mcu" % name)

	def __setattr__(self, name, value):
		if self.portDict.has_key(name):
			# do the assignment
			return self.portDict[name].writeVal(value)
		raise NameError("%s not in Mcu" % name)

	def __repr__(self):
		return 'Mcu()'

if __name__ == '__main__':
	mcu = Mcu()
