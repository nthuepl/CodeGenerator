EcoCast
-------

This is the new implementation of EcoExec/EcoCast code with our own
code generator, instead of invoking existing compilers.

(1/22/2014) Pai

- The cc2540mcu.py is running with real hardware.
- The nrf51822mcu.py is running in text mode but not yet tested.
- The nrf24e1mcu.py is running in text mode but not yet tested.  It
	shares some 8051 code as cc2540mcu.py.

There are separate README-xx.md files for each of the three
architectures.

Naming convention:

- `xxx-mcu.py` (no -) the top-level MCU file for each MCU.
  Currently we have three MCUs supported:
	- `cc2540mcu.py`: which also works with `cc2540sfr.py` (special
		function registers) and `cc2540var.py` (variables)
	- `nrf51822mcu.py`: which also works with `nrf51822sfr.py` and
		`nrf51822var.py`
	- `nrf24e1mcu.py`: which also works with `nrf24e1sfr.py` and
		`nrf24e1var.py`
- `cc_xxxx.py`: the code capsule (code generator) for the given ISA,
  inherited from `codecapsule.py`.  Currently, we have
	- `cc_8051.py` (used by both cc2540mcu.py an nrf24e1mcu.py)
	- `cc_thumb.py` (used by nrf51822mcu.py)
- `isa_xxxx.py`: the ISA definition for the instruction set
	architecture (more or less compiler independent).  Currently, we
	have
	- `isa_8051.py`: (used by both cc2540mcu.py and nrf243e1.mcu.py)
	- `isa_thumb.py`: (used by nrf51822mcu.py and other Cortex-M0)

- `sdcc8051.py`: (still needs to be renamed)
  - this is used by the `nrf24e1mcu.py` as code generator for function
		calls and mapfile API. However it has not been tested, and the
		mapfile should be separated.  It assumes it is compiled
		with stack parameter passing convention. So, invoke your sdcc with
		the flag `% sdcc --stack-auto foo.c`
  - this really should be renamed.
- `mapfile.py`: (still needs to be renamed)
  - this is used by `cc2540mcu.py` as code generator for function
		calls and mapfile API. However, the mapfile should be separated.
