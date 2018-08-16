This is the nRF51822 version of the code generator.

Unlike the 8051, the semantics here mimics general-purpose C and is
thus a little easier, though we do also support bit fields with SFRs.

Test case:

		% python -i nrf51822mcu.py
		>>> mcu.SPIS_ENABLE


