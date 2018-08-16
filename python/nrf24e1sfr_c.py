'''
  nrf24e1sfr_c.py

  This is the new-style SFR class with

	- factored out SFR definition into sfr_def_nrf24e1.py
	- using sdcc8051sfr.py for the code generator for generic 8051 by
		SDCC.

  We are basically recovering the nRF24E1SFR class (colletion of SFRs)
	by plugging the SFR definitio ndictionary into the SDCC8051SFR class.
	This allows the sdcc8051sfr to be composed with cc2540 or other
	8051-based MCU SFR.

	This is the MCU for the old Eco node.

	The data is taken from the data sheet "nrf24e1.pdf", page 11,
	Table 2-1 "SFR Register map"; and also better summary is on
	Table 10-9 "Special Function Registers summary", pages 79-80.

  If you run this file as top level then it generates the header file
	named nrf24e1sfr.h.  Actually, this is the only reason for having
	this subclass in its own file.
'''

import sdcc8051sfr
from sfr_def_nrf24e1 import SFR_DEF_nRF24E1

class nRF24E1SFR(sdcc8051sfr.SDCC8051SFR):
	'''
		This class nRF24E1SFR should be instantiated first and accessing
		the instance variables
	'''
	def __init__(self, mcu=None):
		sdcc8051sfr.SDCC8051SFR.__init__(self, 'nrf24e1',
				SFR_DEF_nRF24E1._SFR, {}, mcu)

if __name__ == '__main__':
	c = nRF24E1SFR()
	c.generateHeader('nrf24e1sfr_c.py')

