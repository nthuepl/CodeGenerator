This is for the CC2540, the MCU used in EcoBT wireless sensor node.

20140228 PC:

- This code has been restructured to maximize sharing with nRF24E1,
	which is also 8051 ISA based.  Now we are doing SDCC code generation.

## Files:

- `cc2540mcu_c.py`: the top-level MCU file that uses SDCC for code
	generation.  This one an run a few operations, but not complete yet;
	it will eventually supercede `cc2540mcu.py`, which is the currently
	working version that uses direct assembly code generation.
- `cc2540sfr_c.py`: the SFR-collection for cc2540 MCU.  It combines
	definitions from two other files:
  - `sfr_def_cc2540.py`: the actual SFR definition dictionary
	- `sdcc8051sfr.py`: the SFR code, shared by all 8051 MCUs using SDCC
		compiler
- `cc2540var.py`: This is a placeholder for now; will need to be
	superceded by `cc2540var_c.py` to model "variables"
- `cc_sdcc8051.py`: this is the code capsule subclass for code
	generation targeting SDCC 8051.  It inherits from Niels's `cc_c.py`.
- `sdcctype.h`: defines the uint8, int8, etc type names that SDCC
	doesn't define.
- `CodeGenerator.py`: this is a misnomer... it is just a placeholder
	for now borrowed from cc2540mcu as an interface to serial port.  It
	is NOT really a code generator!  This really needs to be renamed.

## Setup and running:

- assume SDCC has been installed (I am using 3.3.0) from
	http://sdcc.sourceforge.net/
- need to set up the header file (cc2540sfr.h) once 
	so that the code generator that invokes SDCC will have
	the proper SFR name declarations to generate the right code.
	This just has to be done each time there is a change of SFR defintion.

    % python cc2540sfr_c.py


- There are now new reprMode's of execution.

  - mcu.setReprMode('text'): (default) this now shows C code, but only
		the last item of C code is used due to the use of emit() method.

  - mcu.setReprMode('disasm'): this will invoke SDCC to generate code,
		create binary without any library code, make the .ihx file, use
		sdobjcopy to read from it, and disassemble it as 8051

- Simple things seem to be working: (by default it uses 'text' reprMode)

    % python -i cc2540mcu_c.py
    >>> mcu.ADCCON1.STSEL = mcu.ADCCON1.RTCRL
    CC_SDCC8051(VAR('A')): ['(uint8)(ADCCON1 & 0xc) >> 2', '(ADCCON1 = (ADCCON1 & 0xcf) | (((uint8)(ADCCON1 & 0xc) >> 2) << 4) & 0x30)']
    >>> mcu.setReprMode('disasm')
    >>> mcu.ADCCON1.STSEL = mcu.ADCCON1.RTCRL
    ['MOV A, #0xcf', 'ANL A, 0xb4', 'MOV R7, A', 'MOV A, #0xc', 'ANL A, 0xb4', 'RR A', 'RR A', 'ANL A, #0x3f', 'SWAP A', 'ANL A, #0xf0', 'MOV R6, A', 'MOV A, #0x30', 'ANL A, R6', 'ORL 0x7, A', 'MOV 0xb4, R7', 'MOV DPTR, #0x881', 'MOV A, R7', 'MOVX @DPTR, A', 'RET']

- To do (for the C version):

  - Still need to work on the VAR part of code generation.
		Specifically, combining multiple bitfields from different SFRs into
		the same symbol access.  8051 may have just L and H registers
		combined, but AVR actually combines bitfields from different
		registers!
	- Migrate some code from derived class into base class for
		codecapsule stuff.
  - generate code for function calls -- of different calling
		conventions! array access, pointers, ...


----------------------------------------------------------------------


## File Overview

The classes defined are


		file: cc2540mcu.py
		  CC2540MCU: this is the top-level class that contains all the
			definitions.
			All the SFRs, VARs, etc must be accessed through the MCU 
			such as 
			>>> mcu = CC2540MCU()
			>>> mcu.P1 = mcu.P2 - mcu.x1

			All the SFR names are defined (e.g., mcu.P1, mcu.P2)
			All the registers (R0-R7) are defined as VARs
			Variables x0-x7 are defined for convenience of testing
			to be iram addresses 0x40-0x47

			The MCU's __getattr__ and __setattr__ methods are called when you do
			mcu.port (on RHS) => calls mcu.__getattr__('port')
			mcu.port = expression => calls mcu.__setattr__('port', expression)

`

		file: cc2540sfr.py
		  SFR: this is the special function register class.
			It contains the definitions for SFRs as well as the 		data structures
			for their code generation.
			Each SFR can also contain slices, or potentially 16-		bit and others.
			we have limited ability to handle 16-bit (e.g. DPTR)
			Some single-bit SFRs may also be handled.
			Actually, there is also an XREG class, which is not 		really used for
			instantiation but is only there to provide the definitions for XREGs
			(think of as SFRs with 2-byte address)

			The __getattr__ and __setattr__ functions are called when doing
			either bit index or bit slices
`


		file: cc2540var.py
		  VAR: this is storage element, ranging from single bit, internal-ram
			byte (under 0x80), upper-ram (0x80 to 0xff, but indirectly
			addressable only thru @R0 or @R1), external data, DPTR, etc.

			The __getattr__ and __setattr__ functions are called when doing
			either bit index or bit slices
`


		file: codecapsule.py
		  CodeCapsule: this is the data structure that contains code.
			You can code generate using a string template, which must match
			one of the templates exactly. The template will have the form
			of opcode operand with %x or %d specifier.  Multiple templates
			may correspond to the same instruction, depending on what you want
			to hardwire (e.g., @R0 may be hardwired, or you may have @R%d
			and substitute in a register number). 
			Pass as many of the arguments as the template specifies, and it will
			perform the substitution for the string as well as assembly the
			instruction on-the-fly.  A code capsule stores both.

			What CodeCapsule does not do yet is to handle labels.  What's needed
			is to keep things in some kind of lambda (well, as a curried
			function) if possible, but maybe not. Then, after the symbol is
			resolved, it can then evaluate the string and resolve the address.
			It will be needed later for the absolute addresses or external calls.
			f = lambda x, y: ...
			f1 = lambda x: f(x, constant)

		  It turns out CodeCapsule is the data structure that is returned
			after the mcu.port is invoked.  So this means in order to support
			operator overloading such as +, -, and all the operators, 
			they have to be defined in the CodeCapsule class.
`

## Issues (before using SDCC)

- 16-bit variables are partially working
- signed and unsigned are not always properly handled
- boolean still can't always be handled due to Python disallowing
	override, so we'll have to do this as code generation
- atomic operations are not handled, especially things like
  P2 |= 2
	which can be very useful for setting bits atomically, and plus it
	reads from the port latch rather than from the pins.
	This needs some postprocessing, maybe...
- arrays work for 8 bit or 16 bit like C, but no length check
- structs: need struct schema
- pointers: not yet (except array)
- control construct
- function
- local variables
- object


## Python

### Operator overloading

A Guide about Python Operation Overwriting
[link](http://www.rafekettler.com/magicmethods.html)

### Parser

To generate Python ast in 2.7,

```
compiler.parse(STATEMENT)
```

Since compiler module is removed from python 3.x,
alternative way to do it using ast module

```
code = ast.parse(STATEMENT, 'anyfilename.py')
ast.dump(code)
```

1/4/2014

useful to install the codegen package. it is not part of the standard but it is written
by the ast author (I think)
Download from https://pypi.python.org/pypi/codegen

This page has a good explanation on AST
http://eli.thegreenplace.net/2009/11/28/python-internals-working-with-python-asts/


here is my Python interactive test

		>>> import codegen
		>>> import ast
		>>> code =ast.parse('''x = 3
		... def f(y):
		...     return y * 2
		... ''')

		>>> codegen.to_source(code)
		'x = 3\n\ndef f(y):\n    return y * 2'
		>>> print codegen.to_source(code)
		x = 3

		def f(y):
		    return y * 2
		>>>


-------


## Repr

12/20/2013

(Pai) There is actually an easy way to figure out if you are top-level during
interactive mode.  This is done by keeping a recursive level counter for the
`__repr__` method.  Interactive mode will call `__repr__` to render the
representation.  We can intercept that and

- flatten the code
- turn it into transmit action
- maybe wait until reply
- type-demarshal the reply value

so what I am missing now is more of the type demarshaling part. I have the type
information but I need to build it into the code capsule.

Eventually it should be able to handle not only scalars but also arrays and
structs.

New features as of today

- `mcu.reprMode()` -- defaults to 'text' output of generated code;
  could be set to 'binary'

- `mcu.setReprMode()` - sets the reprMode to either text or binary.
  this is for interactive mode.

- moved the grabReturnValue from function call (mapfile.py) to codecapsule.py's
	`__repr__` method. This is so that even for non-function calls, it will
	grab the return value and stick it into the return buffer (default = 0x28 in
	external data RAM, but this can be changed)
	this is also for allowing function calls to be performed in a chain and don't
	stick their return value into buffer until the whole expression is completely
	evaluated.

- later, `__repr__` can be overridden to allow communication!

## Tests


		% python -i cc2540mcu.py
		>>> mcu.P1
		CodeCapsule(VAR('A')): ['MOV A, 0x90', 'MOV 0x28, #0x1', 'MOV 0x29, A']
		# note: only the first instruction does the move;
		# the second instruction sets the return length in the return buffer,
		# and the third instruction moves A into the return buffer's 2nd byte

		>>> mcu.P0 = mcu.P1 + 3
		CodeCapsule(VAR('A')): ['MOV A, 0x90', 'ADD A, #0x3', 'MOV 0x80, A', 'MOV 0x28,
		#0x1', 'MOV 0x29, A']
		# here, even though it is an assignment, we still return its value anyway!
		# but if you don't want it, we can take it out. I just need to do the
		# setResultType('void') for the readVar or readSFR method

		>>> mcu.DPTR
    CodeCapsule(VAR('R3R2')): ['MOV R3, 0x83', 'MOV R2, 0x82', 'MOV 0x28, #0x2', 'MOV 0x29, R2', 'MOV 0x2a, R3']
		# This tests 16-bit variable access.  As with IAR's convention, 16-bit values
		# are stored in R3:R2 pair.  So, we move them to R3:R2 first, and then 
		# put the three bytes [length][DPL][DPH] into return buffer
		# (because 8051 is little endian)

		>>> mcu.DPTR = mcu.DPTR + 3
		CodeCapsule(VAR('R3R2')): ['MOV R3, 0x83', 'MOV R2, 0x82', 'MOV A, R2', 'ADD A, #0x3',
		'MOV R2, A', 'MOV A, R3', 'ADDC A, #0x0', 'MOV R3, A', 'MOV 0x83, R3', 'MOV 0x82, R2',
		'MOV 0x28, #0x2', 'MOV 0x29, R2', 'MOV 0x2a, R3']
		# this is because we load DPTR into R3:R2, do a 16-bit +3, then move into DPTR
		# again, and then grab the value into return buffer (but again, I think maybe we
		# should eliminate the return value for assignment statements)



## To-do
(Before SDCC version, but some may still be applicable)

- allow the use of single-char string literals to be used in place of int.
  For example, 'a' would correspond to its ASCII code. Empty string
	would be 0.  *This is done*
	
- allow zero-terminated strings to be assigned to char pointers?
  but where would we put the data for the string?

- What we need is a space for a pool of data, addressable by array.
  Internally, `uint8*` would indicate it can be an array (no preset bound)
	and each element is 8 bits. 
	if type is a pointer then it can point to another array of the same type.
	it could be a string literal, int list (as array), whichever.
  You can also do slice assignment to copy content rather than changing
	reference.

To-do tasks

- need to allocate R3:R2 as 16-bit temporary to prevent uint8 from reusing
  them at the same time.

12/22/2013 

(Pai) implemented basic array access.  This is done by

- extending the VAR to handle array definition in the form of a tuple, 
  such as `('uint8', 12)`, making the `readVar()` method to return a
	`CodeCapsule` of result type `uint8*`
- overloading the `__getitem__` and `__setitem__` operators in `CodeCapsule`
  to perform indexing and memory access.  For now, support is limited to just
	uint8 and uint16 arrays, 8-bit or 16-bit values, 
- add the `print self` or `print value` statement before the return statement
	inside the `__setitem__`, because Python shell does not call `__repr__` on the
	return value of `__setitem__`.
- added a few predefined variables, `a0`, `a1`, etc, as arrays (defined in MCU)

Here are some examples


		>>> mcu.a0[1]  = 3
		CodeCapsule(None): ['MOV R2, #0x0', 'MOV R3, #0x1', 'XCH A, R2', 'ADD A, #0x1', 'MOV DPL, A', 'XCH A, R3', 'ADDC A, #0x0', 'MOV DPH, A', 'MOV A, #0x3', 'MOVX @DPTR, A', 'MOV 0x28, #0x1', 'MOV 0x29, A']
		>>> mcu.a0[mcu.P1]  = mcu.P2 + 3
		CodeCapsule(VAR('A')): ['MOV A, 0xa0', 'ADD A, #0x3', 'PUSH ACC', 'MOV A, 0x90', 'PUSH ACC', 'MOV R2, #0x0', 'MOV R3, #0x1', 'POP ACC', 'ADD A, R2', 'MOV DPL, A', 'ADDC A, R3', 'MOV DPH, A', 'POP ACC', 'MOVX @DPTR, A', 'MOV 0x28, #0x1', 'MOV 0x29, A']
		>>> mcu.P1 + 2 - mcu.u3
		CodeCapsule(VAR('A')): ['MOV A, 0x90', 'ADD A, #0x2', 'MOV R7, A', 'MOV R0, #0xc3', 'MOV A, @R0', 'XCH A, R7', 'CLR C', 'SUBB A, R7', 'MOV 0x28, #0x1', 'MOV 0x29, A']


To Do:

- need to have a better way to distinguish between uint16 and pointers in the
	value, and have a method to return the byte size rather than checking the
	hardwired types

- need a way to support pointer variables, not just arrays

- need a way to work with array literals, including strings, lists, etc.

- need to be able to work with structs, maybe in conjunction with the struct
	package.

- need to be able to generate code for array (slice) copying and struct copying.
  how do we represent structs? as a descriptor string?

- need to check array bounds

- need a way to remember the type of the returned data so that it can be
	type-demarshaled (by unpack) to generate the right Python data.

-----------------------

1/19/2014

- the first integration with THM and Neo's code was first run on
	1/17/2014.  It was able to open the serial port, open the connection
	(i.e., pair) with the node, send instructions, and display the
	"raw" return value.
	However, there was bug in everyone's code, so it was not completely
	correct, but at least it executed instructions!  We were able to
	turn on and off several LEDs!!!

- to try the code, 
  1. edit cc2540mcu.py and set `UseSerialPort = True` on line 224
	   and copy THM's code from `../host/*.py` directory
  2. Run the code. at least this is what it looks on mine, with the
	   dongle. yours may look different.  For now, you'll need the EcoBT
		 with dongle firmware to work as dongle
.

        % python -i cc2540mcu.py
        Available COM Ports
        1: /dev/cu.Bluetooth-Incoming-Port
        2: /dev/cu.Bluetooth-Modem
        3: /dev/cu.usbmodem1411
        Select COM Port: 3
        Start device scan
        1: 00:00:00:00:80:20
        Scan Done
        Select node: 1
        >>> mcu.setReprMode('exec')
        >>> mcu.P1
        [229, 114, 114, 122, 4, 240, 34]

  or something like that. (This was buggy machine code; the 122, 4
	sequence should be switched, so the correct machine code should be
	`[229, 144, 144, 4, 122, 240, 34]` where the final 34 is RET instruction)

- It turns out there was a bug in Pai's code for `MOV DPTR, #data16`,
  which ironically is "big endian" for data16!
	I mistakenly generated it as little endian, but this has been fixed.
	I don't have the hardware to try it as of this writing, but will
	try it when I have a chance.


