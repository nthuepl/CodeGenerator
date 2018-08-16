This is for the nRF24E1, the MCU used in the original Eco.

20140228 PC:

- This code has been restructured to maximize sharing with CC2540,
	which is also 8051 ISA based.  Now we are doing SDCC code generation.

## Files:

- `nrf24e1mcu_c.py`: the top-level MCU file (this one can run a few SFR
	operations).  This supercedes `nrf24e1mcu.py`, which was never
	working in the first place.
- `nrf24e1sfr_c.py`: the SFR-collection for nRF24E1 MCU. It combines
	definitions from two other files:
	- `sfr_def_nrf24e1.py`: the actual SFR definition dictionary
	- `sdcc8051sfr.py`: the SFR code, shared by all 8051 MCUs using SDCC
		compiler
- `nrf24e1var.py`: This is a placeholder for now; will need to be
	superceded by `nrf24e1var_c.py` to model "variables"
- `sdcc8051.py`:   This is a placeholder for now; will need to be
	superceded by some mapfile with calling convention for SDCC-8051
	combination.
- `cc_sdcc8051.py`: this is the code capsule subclass for code
	generation targeting SDCC 8051.   It inherits from Niels's `cc_c.py`.
- `sdcctype.h`: need this as a glue for SDCC to use the common type
	names, such as uint8, int8, etc.
- `CodeGenerator.py`: this is a misnomer... it is just a placeholder
	for now borrowed from cc2540mcu as an interface to serial port.  It
	is NOT really a code generator!  This really needs to be renamed.
- `EcoCast/host/Eco/`: pyserial code for the base station
  (need to be put into the code)


## Setup and running:

- assume SDCC has been installed (I am using 3.3.0), from
	http://sdcc.sourceforge.net/
- Need to set up the header file (nrf24e1sfr.h) once by running

    % python nrf24e1sfr_c.py

- to try out interactively.  (### is for comment)

    % python -i nrf24e1mcu_c.py
		### initially, reprMode is 'text' (which is C in this case) ###
		>>> mcu.RADIO.CS
		CC_SDCC8051(VAR('A')): ['RADIO_CS']
		### you can see compiled and disassembled output by setting ###
		### reprMode to 'disasm'  ###
		>>> mcu.setReprMode('disasm')
		>>> mcu.RADIO.CS = 1
		['SETB 0xa3', 'MOV DPTR, #0x28', 'MOV C, 0xa3', 'CLR A', 'RLC A',
		'MOVX @DPTR, A', 'RET']
		>>> mcu.setReprMode('text')
		>>> mcu.RADIO.CS = mcu.P1._2
		CC_SDCC8051(VAR('C')): ['P1_2', '(RADIO_3 = P1_2)']
		### Note that for now the code capsule in 'text' mode you should
		### just look at the last string; all the other strings before are
		### the intermediate expressions building up to the final one.

- to do: integrating and testing the communication code




## Calling convention for SDCC:

Taken from Section 3.15 on page 54 of [SDCC Compiler User Guide](http://sdcc.sourceforge.net/doc/sdccman.pdf)

### First (non-bit) parameter and return value

using the global registers DPL, DPH, B and ACC,
according to the following scheme: 

- one byte return value in DPL, 
- two byte value in DPL (LSB) and DPH (MSB). 
- three byte values (generic pointers) in DPH, DPL and B, and 
- four byte values in DPH, DPL, B and ACC. 
- Generic pointers contain type of accessed memory in B:
  - 0x00 – xdata/far, 
  - 0x40 – idata/near – ,
  - 0x60 – pdata,
  - 0x80 – code.

### Second parameter onwards 

is either allocated 

- on the stack (for reentrant routines or if --stack-auto is used) or 
- in data/xdata memory (depending on the memory model).


### Bit parameters

are passed 

- in a virtual register called 'bits' in bit-addressable space for reentrant functions or
- allocated directly in bit memory otherwise.


Functions (with two or more parameters or bit parameters) that are
called through function pointers must therefore be reentrant so the
compiler knows how to pass the parameters.


