This is the experimental directory on compiling SDCC code to call IAR
functions.  

## Instructions

    cd CC2540; make ; cd ..
		cd CC2541; make ; cd ..
		python -i runflash.py CC2540/testacc.bin ''

(or testrtc.bin, testhello.bin, etc).  You can also make the `.rel` file
if you want from those directories..

### genmapdef.py: Generate mapfile definition as C header file

This GIT repository includes the map file generator by Kao Chung-yi
(高仲毅).  It is assumed to have already generated the `dic.py` file in
the directory `../../code_parser/result_2540/dic.py` (or
`result_2541`), so that the addresses extracted from IAR's mapfiles
can be used symbolically in the form of `$(ARCH)relay.h`.
If these relay files are not built automatically, you can do this:

    cd CC2540; make ../cc2540relay.h; cd ..
    cd CC2541; make ../cc2541relay.h; cd ..

Even though the relay.h file should be made automatically. I don't
know if it works correctly.   It assumes Python is installed, and that
`genmapdef.py` file is in same directory as the source (but probably
should be moved elsewhere).

### runflash.py: script to program a .bin file into flash and execute

The last argument '' is actually a format string for python's
struct.unpack.  Normally, it must match exactly 20 bytes except if you
leave it blank or give it a string then it determines the length by the
content.  In any case, '' is probably sufficient for now.

The advantage to executing python -i is that it leaves you in
interactive mode after the execution.  You can then take a look at the
variable `retVal` after it finishes and display its various bytes in
different formats.

### Adaptation files

- `sdcc2iar.c`:  this provides macros for shell functions that wrap
	around IAR-compiled API (e.g., OSAL, BLE stack, etc) so that
	SDCC-compiled code can invoke them.  It translates the parameters
	passed by SDCC into the convention of IAR upon calling.  Upon
	return, it translates return value from IAR to return value expected
	by SDCC.  It provides one macro for each type signature, whose
	macro-parameter is the target (relay) address of the callee.
	The return value macro is done separately (and may need fixing); but
	we are limited to returning scalars (8, 16, 24, or 32 bits).
	SDCC has to be compiled for the "small" memory model, `--stack-auto`,
	and explicitly annoted `__xdata` variable or pointer declaration.

- `iar2sdcc.h`:  This provides the macros for call-back routines
	compiled by SDCC but invoked by IAR.  It translates IAR calling
	convention to SDCC calling convention. However, it is done as a
	pair: one macro for the incoming call, and one macro for the
	function exit.  The return value part may still need more work.


### Linking:

Neo's design is to use bank 6 as user space.  Each bank is 32K. Each
flash segment is 2KB (hardware defined).  As of 5/14/2014, segment 0
within bank 6 is used as the "jump table" for all callbacks.   Each
takes 6 bytes and can be overwritten by our own programmer, as the way
SDCC lays out the code.  The first three bytes are for jumping to the
actual function we want invoked (with the same type signature), so the
user can register different code if they want. Second three bytes are
a long-jump that works as effectively a return through relay back to
the caller, and it is the same for all.

## IAR assumes 
- data model: large
- calling convention: xdata reentrant 
- constant data: data rom.  This means if you have strings, you have
	to be careful with passing constant strings (code space?) vs
	variable string buffers (xdata space).



## SDCC

- SDCC supports banked code but maybe not in identical ways to IAR.
  Section 4.1.3.1 Hardware and 4.1.3.2 Software.  we can use `--codeseg
  BANK1` or `#pragma codeseg BANK1` to make the codegen happen to bank 1,
	for example.  The banking concept is the same as with IAR and CC254x.

- param and local can be stack allocated, which seems to be assumed by
  IAR.  This is in Section 3.8 of SDCC:
	- ok to declare auto-local as xdata: `__xdata unsigned char i;`
	- medium or large model places auto locals and params in xdata.
    - Default is `--model-small`
		- can use `--model-medium` but must use for all during compile and link
		- `--model-large` 

- we can allow `$` as an identifier character using the flag
  `--fdollars-in-identifiers`

- so far we assume CC2540 or CC2541 label is defined. to pass the
	macro into the compiler, it uses -DCC2540 or -DCC2541.


## Approach

One issue then is parameters get passed on stack. This can be
inefficient and in fact difficult to translate? in fact it would be hard
to extract the parameters from external stack. It is better to
explicitly annotate locals that need to be passed as pointers.
otherwise, code pointer is 24 bits!

It seems that the only solution for our work (SDCC caller to IAR callee)
translation is to compile SDCC in the small model, using internal
stack if necessary, and then convert to external stack assumed by IAR.

Perhaps the thing to do is to define macros: one for parameter
conversion and one for calling/returning (or separate?).
This will eliminate the extra call overhead by hardwiring the call address

