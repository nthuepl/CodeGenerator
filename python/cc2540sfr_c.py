'''
  cc2540sfr_c.py

	This is the restructured SFR class with 

	- factored out SFR definition into sfr_def_cc2540.py
	- using sdcc8051sfr.py for the code generator for generic 8051 by
		SDCC.

	so, we basically recover the CC2540SFR class (this is the
	"collection" of SFRs for CC2540, rather than an instance of an SFR in
	this collection) by plugging the SFR definition dictionary into the
	SDCC8051SFR class.  This also allows the sdcc8051sfr to be composed
	with the nRF24E1 or other 8051-based MCU's SFR to be composed
	accordingly.

	If you run this file as top level then it generates the header file
	named cc2540sfr.h.  Actually, this might be the only reason for
	having this subclass in its own file!   Otherwise, can be easily
	merged into the MCU class.

	The SFR class that used to be part of cc2540sfr.py is now shared
	across 8051 for SDCC; it is not specific to cc2540 or nrf24e1, etc.

'''

import sdcc8051sfr
from sfr_def_cc2540 import SFR_DEF_CC2540


class CC2540SFR(sdcc8051sfr.SDCC8051SFR):
	'''Unlike the cc2540sfr.py version of CC2540SFR, this one should be
	instantiated first and access the instance variables rather than
	accessing the class variables.
	'''
	def __init__(self, mcu=None):
		sdcc8051sfr.SDCC8051SFR.__init__(self, 'cc2540', SFR_DEF_CC2540._SFR,
				SFR_DEF_CC2540._XREG, mcu)


if __name__ == '__main__':
	c = CC2540SFR()
	c.generateHeader('cc2540sfr_c.py')
